import json
import re
from pathlib import Path

from utils import UniversalEncoder


CHANGE_LINKS = [
    (re.compile('<a href="/\w+/O">O</a>'), 'O'),
    (re.compile('<a href="/include/openssl/.+?\.h">(.+?)</a>'), r'\1'),
    (re.compile('<a href="/include/paths\.h">(.+?)</a>'), r'\1'),

    (re.compile('<a href="/man1/ImageMagick">'), '<a href="/man1/convert">'),
    (re.compile('(<a href="/man1/exit)">'), r'\1-posix">'),

    (re.compile('<a href="/include/sys/ipc\.h">'), r'<a href="/man2/ipc">'),
    (re.compile('<a href="/include/sys/io\.h">'), r'<a href="man2/outb">'),
    (re.compile('<a href="/include/sys/(ioctl)\.h">'), r'<a href="man2/\1">'),

    (re.compile('<a href="/man3/ui_create">(.+?)</a>'), r'\1">'),
    (re.compile('<a href="/include/rpc/(\w+)\.h">'), r'<a href="/man3/\1">'),
    (re.compile('<a href="/include/fontconfig/fontconfig\.h">'), r'<a href="/man3/FcInit">'),
    (re.compile('<a href="/include/varargs.h">'), r'<a href="/man3/va_start">'),
    (re.compile('<a href="/man3/md2">'), r'<a href="/man3/MD2">'),

    (re.compile('<a href="/include/utmp\.h">'), r'<a href="/man5/utmp">'),

    (re.compile('(<a href="/man7/(?:fsf-funding|gpl|gfdl))">'), r'\1-gcc">'),
    (re.compile('<a href="/include/X11/.*?\.h">'), r'<a href="/man7/X">'),
    (re.compile('<a href="/include/netinet/in\.h">'), r'<a href="/man7/netinet_in.h-posix">'),
    (re.compile('<a href="/include/arpa/inet\.h">'), r'<a href="/man7/arpa_inet.h-posix">'),

    (re.compile('<a href="/man8/udev">'), r'<a href="/man8/udevadm">'),

    (re.compile('<a href="/man[58]/init">'), '<a href="/man1/init">'),
]


class FindCrossLinks:
    def __init__(self, only_man_1=False):
        self.missing = {}
        self.only_man_1 = only_man_1

        with Path('data/man_links.json').open() as f:
            self.so_links = json.load(f)  # type Dict
        self.href_regex = re.compile('<a href="(/.*?)">')
        self.link_regex = re.compile('<a href="(/.*?)">(.*?)</a>')

        with Path('data/man_metadata.json').open() as f:
            self.man_data = json.load(f)  # type List
        print('finding cross links...')
        self.uris = set(d['uri'] for d in self.man_data)
        self.sorted_uris = sorted(self.uris)
        self.links = {d['uri']: {'inbound': {}} for d in self.man_data}

    def check_all(self):
        html_root = Path('data/html').resolve()
        for data in self.man_data:
            html_path = html_root / 'man' / '{raw_path}.html'.format(**data)
            html_path = html_path.resolve()
            content = html_path.read_text()
            if '<h2>' in content[:200]:
                content = content[content.index('<h2>'):]
            self.replace_cross_links(data, content, find_links=True)
        missing = sorted(self.missing.items(), key=lambda kv: (len(kv[1]), kv[0]))
        for k, v in missing:
            print(k)
            print('    {}'.format('\n    '.join(v)))
        print('{} bad links to {} pages'.format(sum(len(m) for m in self.missing.values()), len(self.missing)))
        print('{} good links on {} pages'.format(sum(len(m) for m in self.links.values()), len(self.links)))

        if not self.only_man_1:
            with Path('data/cross_links.json').open('w') as f:
                json.dump(self.links, f, indent=2, sort_keys=True, cls=UniversalEncoder)

    def replace_cross_links(self, data, content, find_links=False):
        for regex, repl in CHANGE_LINKS:
            content = regex.sub(repl, content)

        this_uri = data['uri']
        # print(this_uri)
        for m in self.href_regex.finditer(content):
            uri, = m.groups()
            if uri not in self.uris:
                content = self.process_missing(this_uri, uri, content)
        if find_links:
            links = {}
            this_page_text = this_uri.split('/', 2)[-1]
            num = re.search('\d', this_uri)
            if num:
                this_page_text = '{} ({})'.format(this_page_text, num.group())
            for m in self.link_regex.finditer(content):
                uri, text = m.groups()
                num = re.search('\d', uri)
                if num:
                    text = '{} ({})'.format(text, num.group())
                links[uri] = text
                try:
                    self.links[uri]['inbound'][this_uri] = this_page_text
                except KeyError as e:
                    raise RuntimeError('error on {}'.format(this_uri)) from e
            if links:
                self.links[this_uri]['outbound'] = links
        return content

    def process_missing(self, this_uri, uri, content):
        if self.only_man_1 and not uri.startswith('/man1/'):
            return content
        re_ex_uri = re.escape(uri)

        mman_uri = re.sub('^/mann/', '/man3/', uri) if uri.startswith('/mann/') else None

        m_inc = re.search('^/include/(?:include/)?(?:linux/)?(.+?)\.h$', uri)
        new_inc_uri = None
        if m_inc:
            v = m_inc.groups()[0].replace('/', '_')
            inc_uris = [
                '/man3/{}.h'.format(v),
                '/man2/{}.h'.format(v),
                '/man7/{}.h'.format(v),
                '/man7/{}.h-posix'.format(v),
                '/man3/{}'.format(v),
                '/man2/{}'.format(v),
                '/man7/{}'.format(v),
                '/man7/{}-posix'.format(v),
            ]
            if v.startswith('sys_'):
                inc_uris += [
                    '/man2/{}'.format(v[4:]),
                ]
            new_inc_uri = next((v for v in inc_uris if v in self.uris), None)

        if uri in self.so_links:
            new_link = self.so_links[uri]
            content = re.sub('(<a href="){}(">.+?</a>)'.format(re_ex_uri), r'\1{}\2'.format(new_link), content)
        elif new_inc_uri:
            content = re.sub('(<a href="){}(">.+?</a>)'.format(re_ex_uri), r'\1{}\2'.format(new_inc_uri), content)
        elif mman_uri and mman_uri in self.uris:
            content = re.sub('(<a href="){}(">.+?</a>)'.format(re_ex_uri), r'\1{}\2'.format(mman_uri), content)
        elif this_uri.endswith('-freebsd'):
            if '{}-freebsd'.format(uri) in self.uris:
                content = re.sub('(<a href="{})(">.+?</a>)'.format(re_ex_uri), r'\1-freebsd\2', content)
            else:
                content = self.remove_link(uri, content)
        elif '{}-postfix'.format(uri) in self.uris:
            content = re.sub('(<a href="{})(">.+?</a>)'.format(re_ex_uri), r'\1-postfix\2', content)
        elif '{}-ssl'.format(uri) in self.uris:
            content = re.sub('(<a href="{})(">.+?</a>)'.format(re_ex_uri), r'\1-ssl\2', content)
            return content
        elif this_uri.endswith(('.index', '-tcl')):
            # FIXME this fixes lots but we could probably do better
            content = self.remove_link(uri, content)
        elif uri.startswith('/man1/') and uri.replace('man1', 'man8') in self.uris:
            new_link = uri.replace('man1', 'man8')
            content = re.sub('(<a href="){}(">.+?</a>)'.format(re_ex_uri), r'\1{}\2'.format(new_link), content)
        elif uri.startswith('/man8/') and uri.replace('man8', 'man1') in self.uris:
            new_link = uri.replace('man8', 'man1')
            content = re.sub('(<a href="){}(">.+?</a>)'.format(re_ex_uri), r'\1{}\2'.format(new_link), content)
        else:
            prefix = uri + '-'
            for _uri in self.sorted_uris:
                if _uri.startswith(prefix):
                    content = re.sub('(<a href="){}(">.+?</a>)'.format(re_ex_uri), r'\1{}\2'.format(_uri), content)
                    return content
            if uri in self.missing:
                self.missing[uri].add(this_uri)
            else:
                self.missing[uri] = {this_uri}
            # print('    "{}"'.format(uri))
            content = self.remove_link(uri, content)
        return content

    @staticmethod
    def remove_link(uri, content):
        return re.sub('<a href="{}">(.+?)</a>'.format(re.escape(uri)), r'\1', content)


def replace_not_http(m):
    link, name = m.groups()
    if link.startswith(('/', 'https://', 'http://')):
        if link.startswith('/') and not link.endswith('/'):
            link += '/'
        return '<a href="{}">{}</a>'.format(link, name)
    else:
        return name


CHANGE_EXTERNAL_LINKS = [
    (re.compile('<a href="git://github\.com/(.*?)\.git(.*?)">(.+?)</a>'),
     r'<a href="https://github.com/\1\2">\3</a>'),
    (re.compile('<a href="git://git.kernel.org/(.*?)/git\.git">(.+?)</a>'),
     r'<a href="http://git.kernel.org/\1">\2</a>'),

    # this is the same as the next line but more verbose, useful when checking what changes to make
    (re.compile('<a href="(.*?)">(.+?)</a>'), replace_not_http),
    # (re.compile('<a href="[^/](?<!http).*?">(.+?)</a>'), r'\1'),
    (re.compile('<a href="https?://(?:pastebin|localhost|example).*?">(.+?)</a>'), r'\1'),
    (re.compile('<a href="(http.*?)">https?://(.+?)</a>'), r'<a href="\1">\2</a>'),
]


def fix_external_links(content):
    for regex, repl in CHANGE_EXTERNAL_LINKS:
        content = regex.sub(repl, content)
    return content


if __name__ == '__main__':
    """
    Check external link fixing.
    """
    with Path('data/man_metadata.json').open() as f:
        man_data = json.load(f)

    html_root = Path('data/html').resolve()
    print('{} pages to go through'.format(len(man_data)))
    REMAINING_LINKS = re.compile('<a href="[^/].*?">.*?</a>')
    for data in man_data:
        html_path = html_root / 'man' / '{raw_path}.html'.format(**data)
        html_path = html_path.resolve()
        content = html_path.read_text()
        content = fix_external_links(content)
        links = REMAINING_LINKS.findall(content)
        if links:
            print('{}\n    {}'.format(str(html_path)[-30:], '\n    '.join(links)))
            print('')
