#!/usr/bin/env python3
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from tqdm import tqdm


def man_to_ansi(path: str, new_path: Path):
    env = {
        'COLUMNS': '1000',
        'LINES': '100',
        'TERM': 'xterm-256color',
        'LANG': 'en_GB.UTF-8',
    }
    cmd = '/home/samuel/code/man-db/src/man', '-P', 'ul', path
    # cmd = 'script', '-e', '-q', '-c', f'man -P ul {name}', '/dev/null'
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, timeout=2)
    body = p.stdout.replace(b'\r\n', b'\n')
    new_path.parent.mkdir(parents=True, exist_ok=True)
    new_path.write_bytes(body)


def run_all():
    src_path = Path('data/man').resolve()
    dst_path = Path('data/ansi')
    dst_path = dst_path.resolve()

    man_group = 1
    with ProcessPoolExecutor(max_workers=12) as executor:
        futures = {}
        while True:
            dir_path = src_path / f'man{man_group}'
            if not dir_path.exists():
                break

            d_count = 0
            for path in dir_path.iterdir():
                new_path = dst_path / path.relative_to(src_path)
                if not new_path.exists():  # skip existing
                    futures[executor.submit(man_to_ansi, str(path), new_path)] = path
                    d_count += 1
            print(f'{dir_path}: loaded {d_count} tasks...')
            man_group += 1

        count = 0
        for future in tqdm(as_completed(futures), total=len(futures)):
            path = futures[future]
            try:
                future.result()
            except Exception as e:
                raise RuntimeError(f'error in {path}') from e
            else:
                count += 1
                # print(count, path)

    print(f'===\nTotal {count} generated files')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        file_path = Path(sys.argv[1])
        main(file_path)
    else:
        run_all()
