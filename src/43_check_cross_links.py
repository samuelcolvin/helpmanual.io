import json
import re
from pathlib import Path


CHANGE_LINKS = [
    (re.compile('<a href="/\w+/O">O</a>'), 'O'),
    (re.compile('<a href="/include/openssl/.+?\.h">(.+?)</a>'), r'\1'),
    (re.compile('<a href="/include/paths\.h">(.+?)</a>'), r'\1'),

    (re.compile('<a href="/man1/ImageMagick">'), '<a href="/man1/convert">'),
    (re.compile('(<a href="/man1/exit)">'), r'\1-posix">'),

    (re.compile('<a href="/include/sys/ipc\.h">'), r'<a href="/man2/ipc">'),
    (re.compile('<a href="/include/sys/io\.h">'), r'<a href="man2/outb">'),

    (re.compile('<a href="/man3/ui_create">(.+?)</a>'), r'\1">'),
    (re.compile('<a href="/include/(pcre|malloc)\.h">'), r'<a href="/man3/\1">'),
    (re.compile('<a href="/include/rpc/(\w+)\.h">'), r'<a href="/man3/\1">'),
    (re.compile('<a href="/include/fontconfig/fontconfig\.h">'), r'<a href="/man3/FcInit">'),


    (re.compile('<a href="/include/utmp\.h">'), r'<a href="/man5/utmp">'),

    (re.compile('<a href="/include/X11/.*?\.h">'), r'<a href="/man7/X">'),
    (re.compile('<a href="/include/netinet/in\.h">'), r'<a href="/man7/netinet_in.h-posix">'),
    (re.compile('<a href="/include/arpa/inet\.h">'), r'<a href="/man7/arpa_inet.h-posix">'),

    (re.compile('<a href="/man[58]/init">'), '<a href="/man1/init">'),
]


class FindCrossLinks:
    def __init__(self):
        self.html_root = Path('data/html').resolve()
        self.links = {}
        self.missing = {}

        with Path('data/man_metadata.json').open() as f:
            man_data = json.load(f)  # type List

        with Path('data/man_links.json').open() as f:
            self.so_links = json.load(f)  # type Dict
        self.link_regex = re.compile('<a href="(/.*?)">(.*?)</a>')

        print('finding cross links...')
        self.uris = set(d['uri'] for d in man_data)
        for data in man_data:
            self.find_cross_links(data)
        missing = sorted(self.missing.items(), key=lambda kv: len(kv[1]))
        for k, v in missing:
            print(k)
            print('    {}'.format('\n    '.join(v)))
        print('{} 404 links to {} pages'.format(sum(len(m) for m in self.missing.values()), len(self.missing)))

    def find_cross_links(self, data):
        html_path = self.html_root / 'man' / '{raw_path}.html'.format(**data)
        try:
            html_path = html_path.resolve()
        except FileNotFoundError:
            return
        this_uri = data['uri']
        content = html_path.read_text()
        new_content = str(content)
        for regex, repl in CHANGE_LINKS:
            new_content = regex.sub(repl, new_content)
        links = set()
        start = content.index('<h2>') if '<h2>' in content[:200] else 0
        for m in self.link_regex.finditer(new_content, pos=start):
            uri, text = m.groups()
            if uri not in self.uris:
                new_content = self.process_missing(this_uri, uri, text, new_content)
            links.add((uri, text))
        self.links[this_uri] = links

    def process_missing(self, this_uri, uri, text, content):
        mman_uri = re.sub('^/mann/', '/man3/', uri) if uri.startswith('/mann/') else None

        m_inc = re.search('^/include/(.+?\.h)$', uri)
        inc_uri = None
        if m_inc:
            inc_uri = '/man7/{}-posix'.format(m_inc.groups()[0].replace('/', '_'))

        if uri in self.so_links:
            new_link = self.so_links[uri]
            content = re.sub('(<a href="){}(">{}</a>)'.format(uri, text), r'\1{}\2'.format(new_link), content)
        elif mman_uri and mman_uri in self.uris:
            content = re.sub('(<a href="){}(">{}</a>)'.format(uri, text), r'\1{}\2'.format(mman_uri), content)
        elif inc_uri and inc_uri in self.uris:
            content = re.sub('(<a href="){}(">{}</a>)'.format(uri, text), r'\1{}\2'.format(inc_uri), content)
        elif this_uri.endswith('-freebsd'):
            if '{}-freebsd'.format(uri) in self.uris:
                content = re.sub('(<a href="{})(">{}</a>)'.format(uri, text), r'\1-freebsd\2', content)
            else:
                content = re.sub('<a href="{}">({})</a>'.format(uri, text), r'\1', content)
        elif '{}-postfix'.format(uri) in self.uris:
            content = re.sub('(<a href="{})(">{}</a>)'.format(uri, text), r'\1-postfix\2', content)
        elif '{}-ssl'.format(uri) in self.uris:
            content = re.sub('(<a href="{})(">{}</a>)'.format(uri, text), r'\1-ssl\2', content)
            return content
        elif this_uri.endswith('.index'):
            # FIXME this fixes lots but we could probably do better
            content = re.sub('<a href="{}">{}</a>'.format(uri, text), text, content)
        elif uri.startswith('/man1/') and uri.replace('man1', 'man8') in self.uris:
            new_link = uri.replace('man1', 'man8')
            content = re.sub('(<a href="){}(">{}</a>)'.format(uri, text), r'\1{}\2'.format(new_link), content)
        elif uri.startswith('/man8/') and uri.replace('man8', 'man1') in self.uris:
            new_link = uri.replace('man8', 'man1')
            content = re.sub('(<a href="){}(">{}</a>)'.format(uri, text), r'\1{}\2'.format(new_link), content)
        elif uri in self.missing:
            self.missing[uri].add(this_uri)
        else:
            self.missing[uri] = {this_uri}
        return content


if __name__ == '__main__':
    FindCrossLinks()
