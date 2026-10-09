#!/usr/bin/env python3
"""vCard (.vcf) -> JSON Lines, 2026-10-09. Stdlib only. One contact per line.

Usage: python3 -I vcf_to_jsonl_2026-10-09.py contacts.vcf > contacts.jsonl
       python3 -I vcf_to_jsonl_2026-10-09.py --selftest

Reads vCard 2.1 / 3.0 / 4.0 as exported by iPhone Share Contact, macOS Contacts,
Google Contacts and iCloud (CardDAV). Keeps every field it does not understand
under "other" (nothing dropped). Each record carries the source file's SHA-256
and the card's line span, so any value can be traced back to the original bytes.
Photos are not decoded; only their byte length is kept.
"""
import base64
import binascii
import hashlib
import json
import quopri
import sys

KEEP = {'FN', 'N', 'ORG', 'TITLE', 'TEL', 'EMAIL', 'ADR', 'NOTE', 'URL', 'BDAY', 'NICKNAME', 'UID'}


def unfold(text):
    """RFC 6350 3.2: a line starting with space or tab continues the previous one.
    vCard 2.1 quoted-printable soft breaks (= at line end) are joined too."""
    out, start = [], []
    for n, raw in enumerate(text.replace('\r\n', '\n').replace('\r', '\n').split('\n'), 1):
        if out and out[-1].endswith('=') and 'QUOTED-PRINTABLE' in out[-1].split(':', 1)[0].upper():
            out[-1] = out[-1][:-1] + raw          # QP soft break first: keeps a leading space
        elif raw[:1] in (' ', '\t') and out:
            out[-1] += raw[1:]
        else:
            out.append(raw)
            start.append(n)
    return list(zip(start, out))


def unescape(v):
    out, i = [], 0
    while i < len(v):
        c = v[i]
        if c == '\\' and i + 1 < len(v):
            nxt = v[i + 1]
            out.append('\n' if nxt in 'nN' else nxt)
            i += 2
        else:
            out.append(c)
            i += 1
    return ''.join(out)


def split_unescaped(v, sep):
    parts, cur, i = [], [], 0
    while i < len(v):
        if v[i] == '\\' and i + 1 < len(v):
            cur.append(v[i:i + 2]); i += 2; continue
        if v[i] == sep:
            parts.append(''.join(cur)); cur = []
        else:
            cur.append(v[i])
        i += 1
    parts.append(''.join(cur))
    return parts


def parse_line(line):
    if ':' not in line:
        return None
    head, value = line.split(':', 1)
    bits = head.split(';')
    name = bits[0].split('.')[-1].upper()          # drop item1. groups
    params, types = {}, []
    for b in bits[1:]:
        if '=' in b:
            k, v = b.split('=', 1)
            k = k.upper()
            if k == 'TYPE':
                types += [t.strip('"').lower() for t in v.split(',')]
            else:
                params[k] = v
        elif b:
            types.append(b.lower())                   # 2.1 bare types: TEL;CELL
    enc = params.get('ENCODING', '').upper()
    if enc == 'QUOTED-PRINTABLE':
        value = quopri.decodestring(value.encode('latin-1', 'replace')).decode(
            params.get('CHARSET', 'utf-8'), 'replace')
    return name, sorted(set(t for t in types if t not in ('pref', 'internet', 'voice'))), params, value


def parse(text):
    cards, cur = [], None
    for lineno, line in unfold(text):
        if not line.strip():
            continue
        p = parse_line(line)
        if p is None:
            if cur is not None:
                cur['other'].append({'line': lineno, 'raw': line})
            continue
        name, types, params, value = p
        if name == 'BEGIN' and value.strip().upper() == 'VCARD':
            cur = {'first_line': lineno, 'fn': '', 'name': [], 'org': '', 'title': '', 'tel': [],
                   'email': [], 'adr': [], 'note': '', 'url': [], 'bday': '', 'nickname': '',
                   'uid': '', 'photo_bytes': 0, 'other': []}
            continue
        if cur is None:
            continue
        if name == 'END' and value.strip().upper() == 'VCARD':
            cur['last_line'] = lineno
            cards.append(cur); cur = None
            continue
        if name == 'FN': cur['fn'] = unescape(value)
        elif name == 'N': cur['name'] = [unescape(x) for x in split_unescaped(value, ';')]
        elif name == 'ORG': cur['org'] = ' / '.join(unescape(x) for x in split_unescaped(value, ';') if x)
        elif name == 'TITLE': cur['title'] = unescape(value)
        elif name == 'TEL': cur['tel'].append({'type': types, 'value': unescape(value).replace('tel:', '')})
        elif name == 'EMAIL': cur['email'].append({'type': types, 'value': unescape(value)})
        elif name == 'ADR':
            f = [unescape(x) for x in split_unescaped(value, ';')] + [''] * 7
            cur['adr'].append({'type': types, 'po_box': f[0], 'extended': f[1], 'street': f[2],
                               'city': f[3], 'region': f[4], 'postal': f[5], 'country': f[6]})
        elif name == 'NOTE': cur['note'] = unescape(value)
        elif name == 'URL': cur['url'].append(unescape(value))
        elif name == 'BDAY': cur['bday'] = value
        elif name == 'NICKNAME': cur['nickname'] = unescape(value)
        elif name == 'UID': cur['uid'] = value
        elif name == 'PHOTO':
            data = value.split(',', 1)[-1] if value.startswith('data:') else value
            try:
                cur['photo_bytes'] = len(base64.b64decode(data, validate=False))
            except (binascii.Error, ValueError):
                cur['photo_bytes'] = -1
        elif name not in ('VERSION', 'PRODID', 'REV'):
            cur['other'].append({'line': lineno, 'raw': line[:500]})
    if cur is not None:
        raise ValueError('card starting at line %d has no END:VCARD' % cur['first_line'])
    return cards


def convert(path):
    raw = open(path, 'rb').read()
    sha = hashlib.sha256(raw).hexdigest()
    text = raw.decode('utf-8-sig', 'replace')
    for c in parse(text):
        c['source_sha256'] = sha
        sys.stdout.write(json.dumps(c, ensure_ascii=False, sort_keys=True) + '\n')


SAMPLE = (
    "BEGIN:VCARD\r\nVERSION:3.0\r\nN:Sample;Ada;;;\r\nFN:Ada Sample\r\nORG:EXAMPLE LAB;\r\n"
    "item1.TEL;type=CELL;type=VOICE;type=pref:+1 (404) 555-0123\r\nitem1.X-ABLabel:mobile\r\n"
    "NOTE:# Earned vs Scraper Identity\\n\\nSealed 26–27 August 2026\\, append-only.\r\n"
    "PHOTO;ENCODING=b;TYPE=JPEG:/9j/4AAQSkZJRg\r\n ABAQ==\r\nEND:VCARD\r\n"
    "BEGIN:VCARD\r\nVERSION:2.1\r\nN:Office;Test\r\nFN:Test Off\r\n ice\r\nTEL;WORK:770-555-0100\r\n"
    "EMAIL;INTERNET:front@example.com\r\nADR;WORK:;;1 Main St;Lawrenceville;GA;30044;USA\r\n"
    "NOTE;ENCODING=QUOTED-PRINTABLE:Line one=0ALine=\r\n two\r\nEND:VCARD\r\n")


def selftest():
    n = 0
    def check(cond, label):
        nonlocal n
        if not cond:
            raise SystemExit('FAIL ' + label)
        n += 1
    cards = parse(SAMPLE)
    check(len(cards) == 2, 'two cards')
    a, b = cards
    check(a['fn'] == 'Ada Sample' and a['name'][:2] == ['Sample', 'Ada'], 'name fields')
    check(a['org'] == 'EXAMPLE LAB', 'org trailing semicolon')
    check(a['tel'] == [{'type': ['cell'], 'value': '+1 (404) 555-0123'}], 'grouped TEL, pref/voice dropped')
    check(a['note'].startswith('# Earned vs Scraper Identity\n\nSealed') and '\\' not in a['note'], 'escapes')
    check(a['photo_bytes'] == 13, 'folded photo line joined and measured')
    check(any('X-ABLabel' in o['raw'] for o in a['other']), 'unknown field kept')
    check(b['tel'][0] == {'type': ['work'], 'value': '770-555-0100'}, '2.1 bare type')
    check(b['fn'] == 'Test Office', 'folded text line joined, fold space removed')
    check(b['email'][0]['value'] == 'front@example.com', 'email')
    check(b['adr'][0]['city'] == 'Lawrenceville' and b['adr'][0]['postal'] == '30044', 'address fields')
    check(b['note'] == 'Line one\nLine two', 'quoted-printable soft break')
    check(a['first_line'] == 1 and b['first_line'] > a['last_line'], 'line spans')
    try:
        parse('BEGIN:VCARD\nFN:x\n'); check(False, 'unterminated refused')
    except ValueError:
        check(True, 'unterminated refused')
    check(parse('') == [] and parse('FN:loose\n') == [], 'no card, no record')
    print(f'PASS {n}/{n}')


if __name__ == '__main__':
    if sys.argv[1:] == ['--selftest']:
        selftest()
    elif len(sys.argv) == 2:
        convert(sys.argv[1])
    else:
        raise SystemExit(__doc__)
