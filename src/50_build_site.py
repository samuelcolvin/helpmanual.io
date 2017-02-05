import hashlib
import json
import re
import shutil
import subprocess
import sys
from collections import OrderedDict
from datetime import datetime
from operator import itemgetter
from pathlib import Path
from textwrap import dedent

from grablib import Grab
from jinja2 import Environment, FileSystemLoader, Markup
from lxml import html

from utils import generate_description
from cross_links import FindCrossLinks

MAN_SECTIONS = {
    1: 'User Commands',
    2: 'System calls',
    3: 'Library calls',
    4: 'Special files',
    5: 'File formats',
    6: 'Games',
    7: 'Miscellaneous',
    8: 'Admin commands',
    9: 'Kernel routines',
}

# for now these are just for references
POPULAR_COMMANDS = {
    'awk',
    'bash',
    'curl',
    'find',
    'grep',
    'iptables',
    'rsync',
    'sed',
}


class GenSite:
    def __init__(self):
        self.debug = 'debug' in sys.argv
        self.fast = 'fast' in sys.argv
        self.hashed_static_files = {}
        self.site_dir = (Path(__file__).parent / '..' / 'site').resolve()

        if self.site_dir.exists():
            shutil.rmtree(str(self.site_dir))

        self.env = Environment(
            loader=FileSystemLoader('templates'),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.env.filters.update(
            static=self._static_filter,
            to_uri=self._to_uri,
            priority=self._get_priority
        )
        grab = Grab('grablib.yml', debug=self.debug)
        grab.download()
        grab.build()
        p = Path('static/css/inline.css')
        self.env.globals.update(
            embedded_css=p.read_text().strip('\n'),
            debug=self.debug,
        )

        self.html_root = Path('data/html').resolve()
        self.pages = []
        self.now = datetime.now().strftime('%Y-%m-%d')

        with Path('data/man_metadata.json').open() as f:
            man_data = json.load(f)  # type List
        man_data.append({
            'description': 'blerp - FILTERS LOCAL OR REMOTE FILES OR RESOURCES USING PATTERNS',
            'extra1': '1692',
            'extra2': 'Imagination',
            'extra3': 'XKCD',
            'man_id': 1,
            'name': 'blerp',
            'raw_path': 'xkcd',
            'uri': 'man1/blerp',
        })
        man_data.sort(key=lambda v: (v['man_id'], v['name']))

        man_uris = {d['name']: d['uri'] for d in man_data}

        with Path('data/exec_data.json').open() as f:
            exec_data = json.load(f)

        exec_names = {d['name'] for d in exec_data.values() if d}
        exec_data2 = []
        with Path('data/builtin_metadata.json').open() as f:
            builtin_data = json.load(f)

        print('generating static files...')
        self.generate_static()

        print('generating builtin pages...')
        for data in builtin_data:
            self.generate_builtin_page(data)

        self.cross_linker = FindCrossLinks()
        with Path('data/cross_links.json').open() as f:
            self.cross_links = json.load(f)  # type Dict

        print('generating man pages...')
        for i, data in enumerate(man_data):
            try:
                self.generate_man_page(data, exec_names)
            except Exception as e:
                raise RuntimeError('error on {}'.format(data['uri'])) from e
            if self.fast and i > 100:
                break

        print('generating help pages...')
        for i, data in enumerate(exec_data.values()):
            if data is not None:
                exec_data2.append(self.generate_exec_page(data, man_uris))
            if self.fast and i > 100:
                break

            if not self.fast:
                print('generating search index...')
                self.generate_search_index(man_data, builtin_data, exec_data2)
        print('generating index page...')
        self.generate_index(man_data, builtin_data, exec_data2)
        print('generating extras...')
        self.generate_extra()
        print('done.')

    def _static_filter(self, path):
        file_path = self.site_dir / path
        if not file_path.exists():
            raise FileNotFoundError('static file "{}" does not exist'.format(path))
        hashed_url = self.hashed_static_files.get(path)
        if hashed_url is None:
            content = file_path.read_bytes()
            hash = hashlib.md5(content).hexdigest()
            name_parts = file_path.stem, '.' + hash[:15], file_path.suffix
            new_path = file_path.parent / ''.join(name_parts)
            new_path.write_bytes(content)
            hashed_url = '/{}'.format(new_path.relative_to(self.site_dir))
            self.hashed_static_files[path] = hashed_url
        return hashed_url

    @staticmethod
    def _to_uri(uri):
        return '/' + uri.strip('/')

    @staticmethod
    def _get_priority(page):
        if page == '/':
            p = 1
        elif page.startswith('/man1/'):
            p = 0.9
        elif page.startswith('/builtin/'):
            p = 0.8
        elif page.startswith('/help/'):
            p = 0.7
        elif page.startswith('/man8/'):
            p = 0.6
        elif page.startswith('/man7/'):
            p = 0.5
        elif page.startswith(('/man2/', '/man3/')):
            p = 0.1
        else:
            p = 0.3
        return '{:0.2f}'.format(p)

    def render(self, rel_path: str, template: str, sitemap_index: int=None, **context):
        template = self.env.get_template(template)

        assert rel_path and not rel_path.startswith('/'), repr(rel_path)
        if rel_path.endswith('/'):
            rel_path = '{}/index.html'.format(rel_path.rstrip('/'))
        path = self.site_dir / rel_path

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(template.render(**context))
        uri = re.sub('(/index)?\.html$', '', '/' + rel_path)
        if sitemap_index is not None:
            self.pages.insert(sitemap_index, uri)
        else:
            self.pages.append(uri)

    def generate_man_page(self, ctx, exec_names):
        html_path = self.html_root / 'man' / '{raw_path}.html'.format(**ctx)
        try:
            html_path = html_path.resolve()
        except FileNotFoundError:
            print('{} does not exist'.format(html_path))
            return
        content = html_path.read_text()
        if '<h2>' in content[:200]:
            content = content[content.index('<h2>'):]
        content = self.cross_linker.replace_cross_links(ctx, content)
        content = re.sub('(</?)h2>', r'\1h4>', content)

        details = [(label, value) for label, value in [
            ('Man Section', Markup('{} &bull; {}'.format(ctx['man_id'], MAN_SECTIONS[ctx['man_id']]))),
            ('Document Date', ctx.get('doc_date')),
            ('extra &bull; Version', ctx.get('extra1')),
            ('extra &bull; Source', ctx.get('extra2')),
            ('extra &bull; Book', ctx.get('extra3')),
        ] if value]
        man_comments = ctx.get('man_comments', None)

        link_info = self.cross_links.get(ctx['uri'], {})
        ctx.update(
            page_title='{name} &bull; man page'.format(**ctx),
            title='{name} man page'.format(**ctx),
            content=content,
            man_comments=man_comments and dedent(man_comments),
            source='man{man_id}'.format(**ctx),
            details=details,
            outbound_links=link_info.get('outbound', {}).items(),
            inbound_links=link_info.get('inbound', {}).items(),
        )
        if ctx['name'] in exec_names:
            ctx['pages'] = [
                {
                    'class': 'active',
                    'text': 'Man Page',
                    'link': '.',
                },
                {
                    'text': 'Help Output',
                    'link': '/help/{}'.format(ctx['name']),
                }
            ]
        self.render(ctx['uri'].lstrip('/') + '/', 'man.jinja', **ctx)

    def generate_builtin_page(self, ctx):
        html_path = self.html_root / ctx['raw_path']
        try:
            html_path = html_path.resolve()
        except FileNotFoundError:
            print('{} does not exist'.format(html_path))
            return
        content = html_path.read_text()
        content = re.sub('(</?)h2>', r'\1h4>', content)

        ctx.update(
            page_title='{name} &bull; man page'.format(**ctx),
            title='{name} man page'.format(**ctx),
            content=content,
        )
        self.render(ctx['uri'].strip('/') + '/', 'builtin.jinja', **ctx)

    def generate_exec_page(self, ctx, man_uris):
        help_lines = ctx['help_msg'].strip('\n').split('\n')
        uri = 'help/{name}/'.format(**ctx)
        man_variant_uri = man_uris.get(ctx['name'], None)
        ctx.update(
            page_title='{name} &bull; help'.format(**ctx),
            title='{name} help'.format(**ctx),
            description=generate_description(help_lines[0], help_lines[1:10]),
            uri=uri,
            pages=[
                {
                    'text': 'Man Page',
                    'class': '' if man_variant_uri else 'disabled',
                    'link': man_variant_uri,
                },
                {
                    'class': 'active',
                    'text': 'Help Output',
                    'link': '#',
                }
            ]
        )
        self.render(uri.lstrip('/'), 'exec.jinja', **ctx)
        return ctx

    def _sort_help(self, data):
        return sorted(data, key=itemgetter('name'))

    def generate_index(self, man_data, builtin_data, exec_data):
        info = []
        for man_id in range(1, 10):
            info.append((
                len([1 for p in man_data if p['man_id'] == man_id]),
                'man{} man pages ({}).'.format(man_id, MAN_SECTIONS[man_id]),
            ))
        info += [
            (len(builtin_data), 'man pages for bash builtins.'),
            (len(exec_data), 'help and version output from executables.')
        ]
        self.render(
            'index.html',
            'index.jinja',
            sitemap_index=0,
            title='helpmanual.io',
            description='man pages and help text for unix commands',
            info=info,
            total_pages='{:0,.0f}'.format(sum(count for count, text in info)),
        )

    def generate_search_index(self, man_data, builtin_data, exec_data):
        man_dir = Path('data/text')
        search_data = []
        for d in man_data:
            man_path = man_dir / 'man' / '{raw_path}.txt'.format(**d)
            body = man_path.read_text()
            keywords = []
            for f in ['raw_path' 'extra1' 'extra2' 'extra3' 'man_comments']:
                v = d.get(f, None)
                if v:
                    keywords.append(d[f])
            search_data.append(OrderedDict([
                ('name', d['name']),
                ('uri', d['uri']),
                ('src', 'man{man_id}'.format(**d)),
                ('description', self.short_description(d['description'])),
                ('keywords', ' '.join(keywords)),
                ('body', body),
            ]))
        for d in builtin_data:
            html_path = (self.html_root / d['raw_path']).resolve()
            doc = html.fromstring(html_path.read_text())
            body = doc.text_content().replace('\n', ' ')
            search_data.append(OrderedDict([
                ('name', d['name']),
                ('uri', d['uri']),
                ('src', 'builtin'),
                ('description', d['description']),
                ('keywords', ''),
                ('body', body),
            ]))
        for d in exec_data:
            body = '{help_msg} {version_msg}'.format(**d)
            body = body.replace('\n', ' ')
            body = re.sub('  +', ' ', body)
            search_data.append(OrderedDict([
                ('name', d['name']),
                ('uri', '/' + d['uri']),
                ('src', 'help'),
                ('description', self.short_description(d['description'])),
                ('keywords', '{help_arg} {version_arg}'.format(**d)),
                ('body', body),
            ]))

        search_dir = self.site_dir / 'search'
        subset = []
        set_index = 0

        def save_set():
            nonlocal set_index, subset
            set_index += 1
            path = search_dir / '{:02}.json'.format(set_index)
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('w') as f:
                json.dump(subset, f, indent=2)
            subset = []

        uris = set()
        for entry in search_data:
            if entry['uri'] in uris:
                print('repeated uri "{uri}"'.format(**entry))
                continue
            uris.add(entry['uri'])
            subset.append(entry)
            if len(subset) >= 500:
                save_set()
        if subset:
            save_set()

    @staticmethod
    def short_description(description):
        if ' - ' in description[:30]:
            description = description[description.index(' - ') + 3:]
        elif '-' in description[:30]:
            description = description[description.index('-') + 1:]
        return description.lstrip(' -')

    def generate_extra(self):
        self.render('sitemap.xml', 'sitemap.xml.jinja', pages=self.pages, now=self.now)
        self.render('robots.txt', 'robots.txt.jinja')
        self.render('humans.txt', 'humans.txt.jinja', now=self.now)
        self.render('404.html', 'stub.jinja', title='404', description='Page not found.')

    def generate_static(self):
        print('compiling js...')
        args = ('./node_modules/.bin/webpack', '--colors')
        if not self.debug and not self.fast:
            args += '--optimize-minimize',
        subprocess.run(args, check=True)
        for path in Path('static/favicons').resolve().iterdir():
            if path.name == 'master.png':
                continue
            new_path = self.site_dir / path.name
            new_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(path.resolve()), str(new_path))
        for path in Path('static/js').resolve().iterdir():
            new_path = self.site_dir / 'static' / 'js' / path.name
            new_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(path.resolve()), str(new_path))


if __name__ == '__main__':
    GenSite()

