#!/usr/bin/env python3.6
import json

from tqdm import tqdm

from utils import DATA_DIR, run
from hm_logging import start_logging, logger

start_logging()


class ExecPaths:
    def __init__(self):
        self.data_path = DATA_DIR / 'exec_data.json'
        with self.data_path.open() as f:
            self.data = json.load(f)

        self.count = 0
        try:
            self.go()
        finally:
            self.write()
            logger.info('found path for {} commands'.format(len(self.data)))

    def write(self):
        with self.data_path.open('w') as f:
            json.dump(self.data, f, sort_keys=True, indent=2)

    def go(self):
        for name in tqdm(self.data.keys()):
            if self.data[name] and not self.data[name].get('path'):
                try:
                    self.data[name]['path'] = run(f'which {name}').strip('\n ')
                except RuntimeError:
                    pass


if __name__ == '__main__':
    ExecPaths()
