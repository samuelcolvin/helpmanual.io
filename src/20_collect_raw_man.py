#!/usr/bin/env python3.6
import gzip
from pathlib import Path


def extract_man():
    src = Path('/usr/share/man/').resolve()
    dst = Path('data/man')
    dst.mkdir(parents=True, exist_ok=True)
    dst = dst.resolve()

    i = 1
    while True:
        dir = src / 'man{}'.format(i)
        if not dir.exists():
            break
        for p in dir.iterdir():
            if not p.is_file() or p.suffix != '.gz':
                continue
            new_path = (dst / p.relative_to(src)).with_suffix('')
            if new_path.exists():
                continue
            print('{} > {}'.format(p, new_path))
            new_path.parent.mkdir(parents=True, exist_ok=True)
            with gzip.open(str(p), mode='r') as f:
                new_path.write_bytes(f.read())
        i += 1


if __name__ == '__main__':
    extract_man()
