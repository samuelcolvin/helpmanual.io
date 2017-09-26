#!/usr/bin/env python3.6
import os
import re
from pathlib import Path

from utils import man_to_txt


class Generate:
    def __init__(self):
        self.src_path = Path('data/man').resolve()
        self.dst_path = Path('data/text/man')
        self.dst_path.mkdir(parents=True, exist_ok=True)
        self.dst_path = self.dst_path.resolve()
        self.count = 0
        i = 1
        while True:
            dir = self.src_path / 'man{}'.format(i)
            if not dir.exists():
                break
            os.chdir(str(dir))
            self.generate_directory(dir)
            i += 1
        print('===\nTotal {} generated files'.format(self.count))

    def generate_directory(self, p: Path):
        print('processing {}...'.format(p))
        count_b4 = self.count
        for pp in p.iterdir():
            if pp.is_file() and pp.name:
                self.generate_file(pp)

        print('  {} files generated'.format(self.count - count_b4))

    def generate_file(self, p: Path):
        rel_path = p.relative_to(self.src_path)
        new_path = self.dst_path / rel_path
        new_path = new_path.with_suffix('{}.txt'.format(new_path.suffix))
        if new_path.exists():
            return

        try:
            text = man_to_txt(p)
        except Exception as e:
            print(f'error generating text for {p}: "{e}"')
            return
        text = re.sub('[\r\n\t]', ' ', text)
        text = re.sub('  +', ' ', text)
        new_path.parent.mkdir(parents=True, exist_ok=True)
        new_path.write_text(text)
        self.count += 1


if __name__ == '__main__':
    Generate()
