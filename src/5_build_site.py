import json
import re
import shutil
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, contextfunction, Markup, escape

MAN_SECTIONS = {
    1: '1 - Executable programs or shell commands',
    2: '2 - System calls (functions provided by the kernel)',
    3: '3 - Library calls (functions within program libraries)',
    4: '4 - Special files (usually found in /dev)',
    5: '5 - File formats and conventions eg /etc/passwd',
    6: '6 - Games',
    7: '7 - Miscellaneous (including macro packages and conventions), e.g. man(7), groff(7)',
    8: '8 - System administration commands',
}


class GenSite:
    def __init__(self):
        with Path('metadata.json').open() as f:
            data = json.load(f)
        self.env = Environment(
            loader=FileSystemLoader('templates'),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.env.filters['static'] = self._static_filter
        self.env.globals['debug'] = self._debug

        self.man_template = self.env.get_template('man.jinja')
        self.list_template = self.env.get_template('list.jinja')
        self.primitive_html_root = Path('man-primitive-html').resolve()
        self.site_dir = Path('site')
        self.pages = []
        # if self.site_dir.exists():
        #     shutil.rmtree(str(self.site_dir))

        for pdata in data:
            self.generate_page(pdata)
            # if pdata['man_id'] != 1:
            #     break
        self.generate_man_list()
        self.generate_man_sub_lists(data)
        self.generate_index(data)
        self.generate_sitemap()

    def _static_filter(self, path):
        return '/static/{}'.format(path.lstrip('/'))

    @contextfunction
    def _debug(self, ctx):
        output = '<pre>\n'
        for k, v in ctx.items():
            output += '"{}": "{}"\n'.format(k, escape(v))
        output += '</pre>\n'
        return Markup(output)

    def generate_man_list(self):
        pages = []
        for man_id in range(1, 9):
            name = 'man{}'.format(man_id)
            pages.append({
                'uri': '/' + name,
                'name': name,
                'description': MAN_SECTIONS[man_id],
            })
        new_path = self.site_dir / 'man/index.html'
        ctx = dict(
            title='GNU manual',
            description='GNU man pages in 8 sections',
            pages=pages,
        )
        new_path.parent.mkdir(parents=True, exist_ok=True)
        new_path.write_text(self.list_template.render(**ctx))
        self.pages.insert(0, '/man')

    def generate_man_sub_lists(self, data):
        pages = []
        man_id = 1
        for pdata in data:
            if pdata['man_id'] != man_id:
                self._generate_a_man_sub_list(man_id, pages)
                man_id = pdata['man_id']
                pages = []
            pages.append(pdata)
        self._generate_a_man_sub_list(man_id, pages)

    def _generate_a_man_sub_list(self, man_id, pages):
        name = 'man{}'.format(man_id)
        new_path = self.site_dir / '{}/index.html'.format(name)
        ctx = dict(
            title=name,
            description=MAN_SECTIONS[man_id],
            crumbs=[{'name': 'man'}],
            pages=pages,
        )
        new_path.parent.mkdir(parents=True, exist_ok=True)
        new_path.write_text(self.list_template.render(**ctx))
        self.pages.insert(0, '/' + name)

    def generate_page(self, ctx):
        html_path = self.primitive_html_root.joinpath(ctx['raw_path'] + '.html')
        try:
            html_path = html_path.resolve()
        except FileNotFoundError:
            print('{} does not exist'.format(html_path))
            return
        content = html_path.read_text()
        if '<h2>' in content[:200]:
            content = content[content.index('<h2>'):]
        content = re.sub('(</?)h2>', r'\1h4>', content)
        ctx.update(
            title='{name} man page'.format(**ctx),
            content=content,
            man_section=MAN_SECTIONS[ctx['man_id']],
            crumbs=[
                {'name': 'man'},
                {'name': 'man{man_id}'.format(**ctx)},
            ]
        )
        new_path = self.site_dir.joinpath(ctx['uri'].strip('/') + '/index.html')
        new_path.parent.mkdir(parents=True, exist_ok=True)
        new_path.write_text(self.man_template.render(**ctx))
        self.pages.append(escape(ctx['uri']))

    def generate_index(self, data):
        new_path = self.site_dir / 'index.html'
        ctx = dict(
            title='helpmanual.io',
            description='man pages and help text for unix commands',
            pages=data[:200],  # TODO better way of list pages here
        )
        template = self.env.get_template('index.jinja')
        new_path.write_text(template.render(**ctx))
        self.pages.insert(0, '/')

    def generate_sitemap(self):
        new_path = self.site_dir / 'sitemap.xml'
        ctx = dict(
            pages=self.pages,
            now=datetime.now().strftime('%Y-%m-%d'),
        )
        template = self.env.get_template('sitemap.jinja')
        new_path.write_text(template.render(**ctx))


if __name__ == '__main__':
    GenSite()

