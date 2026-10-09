#!/usr/bin/env python3
"""KBLD9 compact hardened candidate: exact directional arithmetic + append-only ledger.
Stdlib only. CLI: python kbld9_hardened_candidate.py selftest | demo | run IN.jsonl OUT.jsonl
Not a replacement for uninspected historical rev 4c; no claims of historical seal.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import os
import tempfile
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, localcontext, ROUND_DOWN
from fractions import Fraction
from pathlib import Path

SCHEMA = 'kbld9-candidate/1'
ALG = 'sha256'
SCALE = Fraction(14826, 10000)  # declared MAD-to-sigma approximation

class KBLDError(ValueError): pass
class KBLDEntryGuard(KBLDError): pass
class KBLDIntegrityError(KBLDError): pass
class KBLDSeamUnbound(KBLDError): pass

SEAMS = ('harmonic_damping', 'resonant_cancel_repetition',
         'embed_four_pillar_provenance', 'radial_spherical_token_engine',
         'spherical_voxel_tokenizer', 'modality_aware_clean_and_audit',
         'star_traversal_nuance_enhance')
_REGISTRY = {}

def GOSUB_Bind_Seam(name, implementation):
    if name not in SEAMS or not callable(implementation):
        raise KBLDEntryGuard('unknown seam or noncallable implementation')
    _REGISTRY[name] = implementation
    if _REGISTRY[name] is not implementation:
        raise KBLDIntegrityError('seam read-back mismatch')

def _seam(name):
    if name not in SEAMS: raise KBLDEntryGuard('unknown seam')
    if name not in _REGISTRY: raise KBLDSeamUnbound(name)
    return _REGISTRY[name]

def _check_json(x):
    if x is None or isinstance(x, (str, bool, int)): return
    if isinstance(x, float):
        if not math.isfinite(x): raise KBLDEntryGuard('nonfinite JSON float')
        return
    if isinstance(x, (list, tuple)):
        for v in x: _check_json(v)
        return
    if isinstance(x, dict) and all(isinstance(k, str) for k in x):
        for v in x.values(): _check_json(v)
        return
    raise KBLDEntryGuard('unsupported canonical JSON value')

def canonical(x):
    try:
        _check_json(x)
        return json.dumps(x, ensure_ascii=False, allow_nan=False,
                          sort_keys=True, separators=(',', ':')).encode('utf-8')
    except (UnicodeError, RecursionError, OverflowError) as exc:
        raise KBLDEntryGuard('invalid canonical JSON structure') from exc

def sha(x): return hashlib.sha256(canonical(x)).hexdigest()

def utc(timestamp=None):
    t = timestamp if timestamp is not None else datetime.now(timezone.utc)
    if not isinstance(t, datetime) or t.tzinfo is None or t.utcoffset() is None:
        raise KBLDEntryGuard('timezone-aware datetime required')
    return t.astimezone(timezone.utc).isoformat()

def exact(value):
    """Exact interpretation of provided decimal text; floats use their shortest repr."""
    if isinstance(value, bool): raise KBLDEntryGuard('boolean is not a magnitude')
    if isinstance(value, Fraction): return value
    if isinstance(value, int): return Fraction(value)
    if isinstance(value, float):
        if not math.isfinite(value): raise KBLDEntryGuard('nonfinite')
        value = repr(value)  # already-rounded float cannot be recovered
    if isinstance(value, str):
        if '/' in value:
            try:
                a, b = value.split('/')
                if not a.strip() or not b.strip(): raise ValueError()
                return Fraction(int(a), int(b))
            except (ValueError, ZeroDivisionError) as exc:
                raise KBLDEntryGuard('invalid ratio') from exc
        try: return Fraction(Decimal(value))
        except (InvalidOperation, ValueError, OverflowError, ZeroDivisionError) as exc:
            raise KBLDEntryGuard('invalid numeric string') from exc
    raise KBLDEntryGuard('invalid numeric type')

def ratio_string(v):
    f = exact(v)
    return f'{f.numerator}/{f.denominator}'

def GOSUB_Add_Units(base, magnitude, direction, unit, base_unit=None):
    if not isinstance(unit, str) or not unit or (base_unit is not None and unit != base_unit):
        raise KBLDEntryGuard('unit mismatch')
    if isinstance(direction, bool) or type(direction) is not int or direction not in (-1, 1):
        raise KBLDEntryGuard('direction must be integer +1 or -1')
    amount = exact(magnitude)
    if amount < 0: raise KBLDEntryGuard('magnitude must be nonnegative')
    result = exact(base) + direction * amount
    return {'value': ratio_string(result), 'unit': unit}

def GOSUB_Refine_Truncate(value, places):
    """Truncate *computed* decimal to instrument places, not original measurement.
    The caller must establish the instrument's units and trusted precision.
    """
    if type(places) is not int or not 0 <= places <= 1000:
        raise KBLDEntryGuard('places must be integer 0..1000')
    v = exact(value)
    # Exact integer arithmetic, truncating toward zero. No binary float.
    factor = 10 ** places
    units = abs(v.numerator) * factor // v.denominator
    prefix = '-' if v < 0 and units else ''
    if places == 0: return prefix + str(units)
    whole, frac = divmod(units, factor)
    return f'{prefix}{whole}.{frac:0{places}d}'

def _median(values):
    s = sorted(values)
    n = len(s)
    if not n: raise KBLDEntryGuard('empty median')
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2

def GOSUB_MAD_Sigma_Guard(data, n_sigma='10', zero_mad='flag_different'):
    if not isinstance(data, (list, tuple)): raise KBLDEntryGuard('sequence required')
    ns = exact(n_sigma)
    if ns <= 0: raise KBLDEntryGuard('n_sigma must be positive')
    if zero_mad not in ('flag_different', 'keep_all'):
        raise KBLDEntryGuard('invalid zero MAD policy')
    good, rejected = [], []
    for i, raw in enumerate(data):
        try: good.append((i, exact(raw), raw))
        except KBLDError: rejected.append({'index': i, 'reason': 'invalid_numeric',
                                           'raw': repr(raw)})
    if not good:
        return {'kept': [], 'flagged': [], 'rejected': rejected,
                'median': None, 'mad': None, 'scale': ratio_string(SCALE)}
    med = _median([v for _, v, _ in good])
    mad = _median([abs(v - med) for _, v, _ in good])
    threshold = ns * SCALE * mad
    kept, flagged = [], []
    for i, v, raw in good:
        is_flagged = abs(v - med) > threshold if mad else (zero_mad == 'flag_different' and v != med)
        (flagged if is_flagged else kept).append({'index': i, 'value': ratio_string(v)})
    if len(kept) + len(flagged) + len(rejected) != len(data):
        raise KBLDIntegrityError('count conservation')
    return {'kept': kept, 'flagged': flagged, 'rejected': rejected,
            'median': ratio_string(med), 'mad': ratio_string(mad),
            'scale': ratio_string(SCALE)}

def GOSUB_Provenance_Attach(payload, timestamp=None, context=None, source='unspecified'):
    _check_json(payload)
    context = {} if context is None else context
    _check_json(context)
    if not isinstance(context, dict) or not isinstance(source, str) or not source:
        raise KBLDEntryGuard('invalid context/source')
    t = utc(timestamp)
    return {'schema': SCHEMA, 'content': payload, 'context': context,
            'data': {'payload_sha256': sha(payload)}, 'time': t,
            'validation': {'status': 'RECORDED_NOT_VERIFIED'},
            'provenance': {'source': source, 'schema': SCHEMA, 'hash_algorithm': ALG},
            'integrity': {'algorithm': ALG, 'content_sha256': sha(payload), 'hash_acquired_utc': t},
            'custody': []}

def GOSUB_KBLD_Deterministic_Filter_Layer(data, timestamp=None, require_damping=False):
    decision = GOSUB_MAD_Sigma_Guard(data)
    if require_damping:
        decision = _seam('harmonic_damping')(decision)
        _check_json(decision)
    return GOSUB_Provenance_Attach(decision, timestamp, {'filter': 'MAD',
        'zero_mad': 'flag_different', 'damping': bool(require_damping)})

def GOSUB_Shepherd_10Sigma_Validate(voxel_data, bounds=None):
    if bounds is not None and not isinstance(bounds, dict): raise KBLDEntryGuard('bounds must be mapping')
    return GOSUB_MAD_Sigma_Guard(voxel_data, (bounds or {}).get('n_sigma', '10'))

def GOSUB_Error_Test(current, target=None):
    if target is not None and not callable(target): raise KBLDEntryGuard('target must be callable')
    if current is None: return ['data_is_none']
    if isinstance(current, (list, tuple)):
        return ['empty_sequence'] if not current else [f'invalid_at_{i}' for i, x in enumerate(current)
                  if _invalid(x)]
    if isinstance(current, dict):
        return ['empty_mapping'] if not current else [f'invalid_at_key_{k}' for k, v in current.items()
                  if _invalid(v)]
    return []

def _invalid(x):
    return isinstance(x, float) and not math.isfinite(x)

def GOSUB_Mitigate(current, errors, target=None):
    # No silent deletion: return original and rejection report.
    return {'original': current, 'errors': list(errors), 'status': 'QUARANTINED'}

def GOSUB_Error_Test_Mitigate_Retest_Loop(target, input_data, max_passes=5, strict=True):
    if type(max_passes) is not int or max_passes < 1: raise KBLDEntryGuard('invalid max_passes')
    if target is not None and not callable(target): raise KBLDEntryGuard('invalid target')
    errors = GOSUB_Error_Test(input_data, target)
    if errors:
        return {'status': 'QUARANTINED', 'passes': 1, 'data': GOSUB_Mitigate(input_data, errors),
                'residual_errors': errors}
    result = target(input_data) if target else input_data
    post = GOSUB_Error_Test(result)
    if post:
        return {'status': 'QUARANTINED', 'passes': 1, 'data': GOSUB_Mitigate(result, post),
                'residual_errors': post}
    return {'status': 'CLEAN', 'passes': 0, 'data': result, 'residual_errors': []}

class AppendLedger:
    """One-process append ledger. Concurrent writers require external exclusive locking.
    Each line is a canonical JSON envelope, chained to the previous line's hash.
    Existing files must end in LF. No repair or rewrite is attempted.
    """
    def __init__(self, path):
        self.path = Path(path)

    def read(self):
        if not self.path.exists(): return []
        raw = self.path.read_bytes()
        if raw and not raw.endswith(b'\n'):
            raise KBLDIntegrityError('unterminated tail: append refused')
        rows, prev = [], None
        for line in raw.split(b'\n')[:-1]:
            try:
                row = json.loads(line)
                if canonical(row) != line: raise KBLDIntegrityError('noncanonical row')
                digest = row['hash']
                body = {k: v for k, v in row.items() if k != 'hash'}
                if sha(body) != digest or row['previous_hash'] != prev:
                    raise KBLDIntegrityError('hash-chain mismatch')
                prev = digest
                rows.append(row)
            except (ValueError, KeyError, TypeError) as exc:
                raise KBLDIntegrityError('malformed ledger row') from exc
        return rows

    def append(self, kind, payload, timestamp=None):
        if kind not in ('ACTIVE', 'supersede_notice', 'quarantine', 'custody'):
            raise KBLDEntryGuard('invalid event kind')
        rows = self.read()
        event = {'schema': SCHEMA, 'kind': kind, 'payload': payload,
                 'time': utc(timestamp), 'previous_hash': rows[-1]['hash'] if rows else None,
                 'sequence': len(rows) + 1}
        event['hash'] = sha(event)
        line = canonical(event) + b'\n'
        # O_APPEND prevents seeking backward, but does not provide multiwriter transaction isolation.
        fd = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
        try:
            written = os.write(fd, line)
            if written != len(line): raise KBLDIntegrityError('short append')
            os.fsync(fd)
        finally: os.close(fd)
        if self.read()[-1] != event: raise KBLDIntegrityError('append read-back mismatch')
        return event

    def supersede(self, old_id, new_id, new_payload):
        if not isinstance(old_id, str) or not isinstance(new_id, str) or not old_id or not new_id or old_id == new_id:
            raise KBLDEntryGuard('invalid supersession ids')
        rows = self.read()
        active = {r['payload']['record_id'] for r in rows if r['kind'] == 'ACTIVE'
                  and isinstance(r['payload'], dict) and isinstance(r['payload'].get('record_id'), str)}
        if old_id not in active or new_id in active: raise KBLDEntryGuard('missing old or duplicate new')
        if any(r['kind'] == 'supersede_notice' and r['payload'].get('old_id') == old_id for r in rows):
            raise KBLDEntryGuard('already superseded')
        # Preflight both records before the first append; preserves the old prefix on invalid input.
        notice = {'old_id': old_id, 'new_id': new_id}
        replacement = {'record_id': new_id, 'value': new_payload}
        canonical(notice); canonical(replacement)
        # Crash between these appends remains an open transaction risk.
        self.append('supersede_notice', notice)
        return self.append('ACTIVE', replacement)

    def view(self):
        rows = self.read()
        actives, notices = {}, []
        for r in rows:
            if r['kind'] == 'ACTIVE':
                rid = r['payload']['record_id']
                if rid in actives: raise KBLDIntegrityError('duplicate record id')
                actives[rid] = r['payload']['value']
            if r['kind'] == 'supersede_notice': notices.append(r['payload'])
        old_ids, new_ids = set(), set()
        for notice in notices:
            old, new = notice['old_id'], notice['new_id']
            if old in old_ids or new in new_ids or old == new:
                raise KBLDIntegrityError('branch/replay/self supersession')
            old_ids.add(old); new_ids.add(new)
            if old not in actives or new not in actives:
                raise KBLDIntegrityError('incomplete supersession')
        return {k: v for k, v in actives.items() if k not in old_ids}

def _expect_error(fn, cls=KBLDError):
    try: fn()
    except cls: return
    raise AssertionError('expected rejection did not occur')

def selftest():
    tests = []
    def test(name, fn):
        fn(); tests.append(name)
    test('canonical ordering', lambda: _assert(canonical({'b': 1, 'a': 2}) == canonical({'a': 2, 'b': 1})))
    test('unicode roundtrip', lambda: _assert(json.loads(canonical({'字': '🙂'})) == {'字': '🙂'}))
    test('invalid JSON rejected', lambda: [_expect_error(lambda v=v: canonical(v)) for v in (float('nan'), float('inf'), {1: 'x'}, {1, 2})])
    test('huge integer exact', lambda: _assert(exact(10**200) == 10**200))
    test('third exact', lambda: _assert(exact('1/3') * 3 == 1))
    test('direction symmetry', lambda: _assert(exact(GOSUB_Add_Units('10', '3/7', 1, 'm')['value']) - 10 ==
        10 - exact(GOSUB_Add_Units('10', '3/7', -1, 'm')['value'])))
    test('unit mismatch', lambda: _expect_error(lambda: GOSUB_Add_Units('1', '1', 1, 's', 'm')))
    test('negative magnitude rejected', lambda: _expect_error(lambda: GOSUB_Add_Units('1', '-1', -1, 'm')))
    test('invalid direction rejected', lambda: [_expect_error(lambda d=d: GOSUB_Add_Units('1', '1', d, 'm')) for d in (True, 0, 2, -2)])
    test('truncate positive', lambda: _assert(GOSUB_Refine_Truncate('12.34567', 4) == '12.3456'))
    test('truncate negative toward zero', lambda: _assert(GOSUB_Refine_Truncate('-12.34567', 4) == '-12.3456'))
    test('no input digit removed', lambda: _assert(GOSUB_Refine_Truncate('0.1', 1) == '0.1'))
    test('MAD outlier', lambda: _assert(len(GOSUB_MAD_Sigma_Guard(['10','10','10','100000000000000000000000'])['flagged']) == 1))
    test('MAD reject nan', lambda: _assert(len(GOSUB_MAD_Sigma_Guard([1, float('nan'), 2])['rejected']) == 1))
    test('MAD count', lambda: _assert(sum(len(GOSUB_MAD_Sigma_Guard([1, 2, 3, 'bad'])[k]) for k in ('kept','flagged','rejected')) == 4))
    test('no silent mitigation', lambda: _assert(GOSUB_Error_Test_Mitigate_Retest_Loop(None, [1,float('nan')])['status'] == 'QUARANTINED'))
    test('bool passes rejected', lambda: _expect_error(lambda: GOSUB_Error_Test_Mitigate_Retest_Loop(None, [], True)))
    test('unbound seam fails', lambda: _expect_error(lambda: GOSUB_KBLD_Deterministic_Filter_Layer([1], require_damping=True), KBLDSeamUnbound))
    test('aware timestamp required', lambda: _expect_error(lambda: utc(datetime(2026, 1, 1))))
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / 'journal.jsonl'; led = AppendLedger(p)
        first = led.append('ACTIVE', {'record_id': 'r1', 'value': '10/1'})
        before = p.read_bytes()
        led.supersede('r1', 'r2', '11/1')
        after = p.read_bytes()
        test('prefix byte invariant', lambda: _assert(after[:len(before)] == before))
        test('derived view', lambda: _assert(led.view() == {'r2': '11/1'}))
        test('old row intact', lambda: _assert(led.read()[0] == first))
        test('replay rejected', lambda: _expect_error(lambda: led.supersede('r1','r3','12/1')))
        test('chain tamper detected', lambda: _tamper_test(p, led))
        q = Path(td) / 'unterminated.jsonl'; q.write_bytes(b'{"old":1}')
        test('unterminated tail refused', lambda: _expect_error(lambda: AppendLedger(q).append('ACTIVE', {'record_id':'x'}), KBLDIntegrityError))
        test('unterminated tail unchanged', lambda: _assert(q.read_bytes() == b'{"old":1}'))
        s = Path(td) / 'partial.jsonl'; s.write_bytes(before + b'{"schema":')
        test('torn append detected', lambda: _expect_error(lambda: AppendLedger(s).read(), KBLDIntegrityError))
        z = Path(td) / 'incomplete.jsonl'; zl = AppendLedger(z)
        zl.append('ACTIVE', {'record_id': 'old', 'value': 1})
        zl.append('supersede_notice', {'old_id':'old', 'new_id':'new'})
        test('incomplete supersession detected', lambda: _expect_error(lambda: zl.view(), KBLDIntegrityError))
    print(f'PASS {len(tests)}/{len(tests)} deterministic tests')
    return len(tests)

def _assert(cond):
    if not cond: raise AssertionError('assertion failed')

def _tamper_test(path, ledger):
    raw = path.read_bytes()
    try:
        path.write_bytes(raw.replace(b'"r1"', b'"xx"', 1))
        _expect_error(lambda: ledger.read(), KBLDIntegrityError)
    finally: path.write_bytes(raw)

def _unique_object_pairs(pairs):
    out = {}
    for k, v in pairs:
        if k in out: raise KBLDEntryGuard('duplicate JSON key')
        out[k] = v
    return out

def run_file(src, dst):
    if Path(src).resolve() == Path(dst).resolve(): raise KBLDEntryGuard('input and output must differ')
    ledger = AppendLedger(dst)
    with open(src, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            try:
                obj = json.loads(line, parse_float=str, parse_int=str,
                                 object_pairs_hook=_unique_object_pairs, parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))
                if not isinstance(obj, list): raise KBLDEntryGuard('input line must be numeric array')
                result = GOSUB_KBLD_Deterministic_Filter_Layer(obj)
                ledger.append('ACTIVE', {'record_id': f'row-{i}', 'value': result})
            except (ValueError, TypeError, KBLDError) as exc:
                ledger.append('quarantine', {'line': i, 'reason': str(exc), 'raw': line.rstrip('\n')})
    print(f'OUTPUT_OK rows={len(ledger.read())} path={dst}')

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='command', required=True)
    sub.add_parser('selftest')
    sub.add_parser('demo')
    run = sub.add_parser('run'); run.add_argument('input'); run.add_argument('output')
    a = ap.parse_args()
    if a.command == 'selftest': selftest()
    elif a.command == 'demo':
        print(json.dumps(GOSUB_Add_Units('10','3/7',-1,'meters')))
        print(json.dumps(GOSUB_KBLD_Deterministic_Filter_Layer(['10','10.1','9.9','1000000']), indent=2))
    else: run_file(a.input, a.output)

if __name__ == '__main__': main()
