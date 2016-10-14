import os
from pathlib import Path

import man2html
from utils import man_to_txt, txt_to_html


class Generate:
    def __init__(self):
        self.src_path = Path('data/man').resolve()
        self.dst_path = Path('data/html/man')
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
                new_path = self.generate_file(pp)
                if new_path:
                    print('{} not generated with man2html, trying text'.format(new_path))
                    self.fallback_generate_file(pp, new_path)

        print('  {} files generated'.format(self.count - count_b4))

    def generate_file(self, p: Path):
        rel_path = p.relative_to(self.src_path)
        new_path = self.dst_path / rel_path
        new_path = new_path.with_suffix('{}.html'.format(new_path.suffix))
        if new_path.exists():
            return
        if p.name in {'dmsetup.8', 'latex2man.1', 'groff_hdtbl.7', 'groff.7', 'awk.1posix', 'printf.1posix'}:
            return new_path
        print(p)
        try:
            html = man2html.man2html_file(p)
        except (UnicodeDecodeError, man2html.ManpageInvalid) as e:
            # print(e)
            return new_path
        new_path.parent.mkdir(parents=True, exist_ok=True)
        new_path.write_text(html)
        self.count += 1

    def fallback_generate_file(self, p: Path, new_path: Path):
        text = man_to_txt(p)
        html = txt_to_html(text)
        new_path.parent.mkdir(parents=True, exist_ok=True)
        new_path.write_text(html)
        self.count += 1


if __name__ == '__main__':
    Generate()
