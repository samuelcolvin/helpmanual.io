import gzip
from pathlib import Path


def extract_man():
    src = Path('/usr/share/man/').resolve()
    dst = Path('./raw/man')
    dst.mkdir(parents=True, exist_ok=True)
    dst = dst.resolve()
    for i in range(1, 9):
        dir = src / 'man{}'.format(i)
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


if __name__ == '__main__':
    extract_man()
