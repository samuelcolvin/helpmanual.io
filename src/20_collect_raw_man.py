#!/usr/bin/env python3
import gzip
import sys
from pathlib import Path
from utils import DATA_DIR


def extract_man(dst_dir):
    src = Path('/usr/share/man/').resolve()
    dst_dir.mkdir(parents=True, exist_ok=True)
    changes = []
    update = 'update' in sys.argv

    i = 1
    while True:
        added, updated = 0, 0
        dir = src / f'man{i}'
        if not dir.exists():
            break
        for p in dir.iterdir():
            if not p.is_file() or p.suffix != '.gz':
                continue
            new_path = (dst_dir / p.relative_to(src)).with_suffix('')
            if not new_path.exists():
                # print('{} > {}'.format(p, new_path))
                added += 1
                new_path.parent.mkdir(parents=True, exist_ok=True)
                with gzip.open(str(p), mode='r') as f:
                    new_path.write_bytes(f.read())
            elif update:
                with gzip.open(str(p), mode='r') as f:
                    new_content = f.read()
                old_content = new_path.read_bytes()
                if new_content != old_content:
                    # print('{} > {} CHANGED'.format(p, new_path))
                    updated += 1
                    new_path.write_bytes(new_content)

        changes.append((f'man{i}', {'added': added, 'updated': updated}))
        i += 1

    print(f'\nchanges:')
    for name, data in changes:
        print(f'  {name}: {data}')


if __name__ == '__main__':
    extract_man(DATA_DIR / 'man')
