#!/usr/bin/env python3
import json

from tqdm import tqdm

from utils import DATA_DIR, run
from hm_logging import start_logging

start_logging()


def exec_paths():
    for p in tqdm(list((DATA_DIR / 'exec').iterdir())):
        name = p.stem
        with p.open() as f:
            data = json.load(f)
        if not data or data.get('path'):
            continue
        try:
            data['path'] = run(f'which {name}').strip('\n ')
        except RuntimeError:
            pass
        else:
            with p.open('w') as f:
                json.dump(data, f)


if __name__ == '__main__':
    exec_paths()
