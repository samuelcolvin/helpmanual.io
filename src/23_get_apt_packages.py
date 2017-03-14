#!/usr/bin/env python3.6
import json

from tqdm import tqdm

from utils import DATA_DIR, run
from hm_logging import start_logging, logger

start_logging()


class GetAptPackages:
    def __init__(self):
        self.data_path = DATA_DIR / 'apt_packages.json'
        if self.data_path.exists():
            with self.data_path.open() as f:
                self.packages = json.load(f)
        else:
            self.packages = {}
        try:
            self.go()
        finally:
            self.write()
            logger.info('generated info for %s packages', len(self.packages))

    def write(self):
        with self.data_path.open('w') as f:
            json.dump(self.packages, f, sort_keys=True, indent=2)

    def go(self):
        packages_names = run('apt list --installed')
        packages_names = [p.split('/', 1) for p in packages_names.split('\n') if p][1:]
        logger.info('%d packages to get info for', len(packages_names))

        for p_name, extra in tqdm(packages_names):
            if not p_name:
                continue
            extra, auto = extra.split('[', 1)
            info = self.packages.get(p_name, {})
            info.update({
                'name': p_name,
                'extra': extra.strip(' \n'),
                'automatic': 'automatic' in auto,
                'apt-show': info.get('apt-show') or run(f'apt show {p_name}'),
                'dlocate-ls': info.get('dlocate-ls') or self.run_list(f'dlocate -ls {p_name}'),
                'dlocate-lsman': info.get('dlocate-lsman') or self.run_list(f'dlocate -lsman {p_name}'),
                'dlocate-lsbin': info.get('dlocate-lsbin') or self.run_list(f'dlocate -lsbin {p_name}'),
            })
            self.packages[p_name] = info

    @staticmethod
    def run_list(cmd):
        try:
            return list(filter(bool, run(cmd).split('\n')))
        except RuntimeError:
            return []

if __name__ == '__main__':
    GetAptPackages()
