import json
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

man_dirs = {
    'man1': '1 - Executable programs or shell commands',
    'man2': '2 - System calls (functions provided by the kernel)',
    'man3': '3 - Library calls (functions within program libraries)',
    'man4': '4 - Special files (usually found in /dev)',
    'man5': '5 - File formats and conventions eg /etc/passwd',
    'man6': '6 - Games',
    'man7': '7 - Miscellaneous (including macro packages and conventions), e.g. man(7), groff(7)',
    'man8': '8 - System administration commands',
}


class GenSite:
    def __init__(self):
        with Path('metadata.json').open() as f:
            data = json.load(f)
        self.env = Environment(loader=FileSystemLoader('templates'), autoescape=True)
        self.env.filters['static'] = self._static_filter

        self.man_template = self.env.get_template('man.jinja')
        self.primitive_html_root = Path('man-primitive-html').resolve()
        self.site_dir = Path('site')
        # if self.site_dir.exists():
        #     shutil.rmtree(str(self.site_dir))

        for i, pdata in enumerate(data):
            self.generate_page(pdata)
            if i > 100:
                break

    def _static_filter(self, path):
        return '/static/{}'.format(path.lstrip('/'))

    def generate_page(self, ctx):
        html_path = self.primitive_html_root.joinpath(ctx['raw_path'] + '.html')
        try:
            html_path = html_path.resolve()
        except FileNotFoundError:
            print('{} does not exist'.format(html_path))
            return
        ctx.update(
            title='{name} man page'.format(**ctx),
            content=html_path.read_text(),
        )
        new_path = self.site_dir.joinpath(ctx['uri'].lstrip('/') + '.html')
        new_path.parent.mkdir(parents=True, exist_ok=True)
        new_path.write_text(self.man_template.render(**ctx))


if __name__ == '__main__':
    GenSite()

