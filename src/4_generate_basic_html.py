import os
from importlib import reload
from pathlib import Path

import man2html


class Generate:
    def __init__(self):
        self.src_path = Path('./raw/man').resolve()
        self.dst_path = Path('./man-primative-html')
        self.dst_path.mkdir(parents=True, exist_ok=True)
        self.dst_path = self.dst_path.resolve()
        self.count = 0
        for i in range(1, 9):
            dir = self.src_path / 'man{}'.format(i)
            os.chdir(str(dir))
            self.generate_directory(dir)
        print('===\nTotal {} generated files'.format(self.count))

    def generate_directory(self, p: Path):
        print('processing {}...'.format(p))
        count_b4 = self.count
        for pp in p.iterdir():
            if pp.is_file() and pp.name:
                self.generate_file(pp)
        print('  {} files generated'.format(self.count - count_b4))

    def generate_file(self, p: Path):
        if p.name in {'dmsetup.8'}:
            print('skipping {}'.format(p.name))
            return
        rel_path = p.relative_to(self.src_path)
        new_path = self.dst_path / rel_path
        new_path = new_path.with_suffix('{}.html'.format(new_path.suffix))
        if new_path.exists():
            return
        print(p)
        try:
            html = man2html.man2html_file(p)
        except man2html.ManpageInvalid as e:
            print(e)
            return
        reload(man2html)
        new_path.parent.mkdir(parents=True, exist_ok=True)
        new_path.write_text(html)
        self.count += 1


if __name__ == '__main__':
    Generate()
