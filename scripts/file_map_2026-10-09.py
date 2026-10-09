#!/usr/bin/env python3
"""FILE MAP, 2026-10-09. One line per file so a seat can pick for itself.

Usage: python3 -I file_map_2026-10-09.py ROOT [ROOT ...] > map.tsv
Columns: root, path, bytes, sha256, kind, how_to_test
how_to_test is a hint read from the file, never a claim that it passes:
  unittest  -> python3 -m unittest discover -s <its folder>
  selftest  -> the file names a selftest() and runs as __main__
  main      -> runs as __main__ (read it before running)
  basic / cpp / sh -> per that folder's RUN or README
  -         -> data or document
Stdlib only. Reads files; writes nothing but stdout. Skips .git and __pycache__.
"""
import hashlib
import os
import sys

SKIP_DIRS = {'.git', '__pycache__', 'node_modules'}
KIND = {'.py': 'python', '.cpp': 'cpp', '.hpp': 'cpp', '.h': 'cpp', '.c': 'c',
        '.bas': 'basic', '.BAS': 'basic', '.sh': 'sh', '.md': 'doc', '.txt': 'text',
        '.json': 'json', '.jsonl': 'jsonl', '.csv': 'csv', '.png': 'image',
        '.jpg': 'image', '.jpeg': 'image', '.zip': 'zip', '.html': 'html'}


def test_hint(full, kind, name):
    if kind == 'python':
        try:
            src = open(full, 'r', encoding='utf-8', errors='replace').read()
        except OSError:
            return '-'
        if name.startswith('test') or 'import unittest' in src:
            return 'unittest'
        if 'def selftest' in src and "__name__" in src:
            return 'selftest'
        if "__name__" in src:
            return 'main'
        return 'import-only'
    if kind in ('basic', 'cpp', 'c', 'sh'):
        return kind
    return '-'


def walk(root):
    root = os.path.abspath(root)
    label = os.path.basename(root)
    for here, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(files):
            full = os.path.join(here, name)
            if os.path.islink(full) or not os.path.isfile(full):
                continue
            h = hashlib.sha256()
            with open(full, 'rb') as f:
                for block in iter(lambda: f.read(1 << 20), b''):
                    h.update(block)
            kind = KIND.get(os.path.splitext(name)[1], 'other')
            rel = os.path.relpath(full, root)
            yield (label, rel, str(os.path.getsize(full)), h.hexdigest(), kind,
                   test_hint(full, kind, name))


def main(roots):
    if not roots:
        raise SystemExit('usage: file_map_2026-10-09.py ROOT [ROOT ...]')
    out = sys.stdout
    out.write('root\tpath\tbytes\tsha256\tkind\thow_to_test\n')
    count = 0
    for r in roots:
        if not os.path.isdir(r):
            raise SystemExit('not a folder: ' + r)
        for row in walk(r):
            if any('\t' in c or '\n' in c for c in row):
                raise SystemExit('tab or newline in a path, refused: ' + repr(row[1]))
            out.write('\t'.join(row) + '\n')
            count += 1
    sys.stderr.write(f'FILE_MAP rows={count}\n')


if __name__ == '__main__':
    main(sys.argv[1:])
