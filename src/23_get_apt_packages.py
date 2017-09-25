#!/usr/bin/env python3.6
import json
import queue
import threading

from tqdm import tqdm

from utils import DATA_DIR, run, load_json_dir
from hm_logging import start_logging, logger

start_logging()
THREADS = 7


class GetAptPackages:
    def __init__(self):
        self.data_path = DATA_DIR / 'apt_packages'
        self.packages = load_json_dir(self.data_path)
        try:
            self.go()
        finally:
            logger.info('generated info for %s packages', len(list(self.data_path.iterdir())))

    def worker(self):
        while True:
            args = self.queue.get()
            if args is None:
                break
            try:
                self.process(*args)
            finally:
                self.queue.task_done()

    def go(self):
        self.queue = queue.Queue(maxsize=10)
        threads = []
        for i in range(THREADS):
            t = threading.Thread(target=self.worker)
            t.start()
            threads.append(t)

        packages_names = run('apt list --installed')
        packages_names = [p.split('/', 1) for p in packages_names.split('\n') if p][1:]
        logger.info('%d packages to get info for', len(packages_names))

        for p_name, extra in tqdm(packages_names):
            if not p_name:
                continue
            self.queue.put((p_name, extra))

        logger.info('waiting for %s queued jobs to finish', self.queue.qsize())
        self.queue.join()

        for i in range(THREADS):
            self.queue.put(None)

        for t in threads:
            t.join()

    def process(self, p_name, extra):
        extra, auto = extra.split('[', 1)
        info = self.packages.get(p_name, {})
        try:
            info.update({
                'name': p_name,
                'extra': extra.strip(' \n'),
                'automatic': 'automatic' in auto,
                'apt-show': info.get('apt-show') or run(f'apt show {p_name}'),
                'dlocate-ls': info.get('dlocate-ls') or self.run_list(f'dlocate -ls {p_name}'),
                'dlocate-lsman': info.get('dlocate-lsman') or self.run_list(f'dlocate -lsman {p_name}'),
                'dlocate-lsbin': info.get('dlocate-lsbin') or self.run_list(f'dlocate -lsbin {p_name}'),
            })
        except Exception as e:
            logger.error('error on "%s": %s', p_name, e)
        else:
            with (self.data_path / f'{p_name}.json').open('w') as f:
                json.dump(info, f, sort_keys=True, indent=2)

    @staticmethod
    def run_list(cmd):
        try:
            return list(filter(bool, run(cmd).split('\n')))
        except RuntimeError:
            return []


if __name__ == '__main__':
    GetAptPackages()
