import json
import re
from pathlib import Path
from html import escape, unescape

#!/usr/bin/env python3.6
import click

c = re.compile
HTTP_START = c('^https?://.+$')
STRIP = '().,\'"\\'


def replace_non_http(m):
    link, name = m.groups()
    if link.startswith('/'):
        return '<a href="{}/">{}</a>'.format(link.rstrip('/'), name)
    if HTTP_START.match(link) and link.strip(STRIP) not in {'http://', 'https://'}:
        return '<a href="{}" target="_blank">{}</a>'.format(link.strip(STRIP), name.strip(STRIP).strip('/'))
    else:
        return name


INVALID_URLS = (
    r'pastebin',
    r'localhost',
    r'example\.',
    r'www\.example',
    r'site\.com',
    r'www\.site\.com',
    r'host\.',
    r'host/',
    r'HOST',
    r'\[USER@\]HOST',
    r'foo\.com',
    r'foo\.bar',
    r'bar\.com',
    r'api\.github\.com',
)


CHANGE_EXTERNAL_LINKS = [
    # correct github git links
    (c('<a href="git://github\.com/(.*?)">(.+?)</a>'), r'<a href="https://github.com/\1">\2</a>'),

    # correct kernel.org git links
    (c('<a href="git://git.kernel.org/(.*?)/git\.git">(.+?)</a>'), r'<a href="http://git.kernel.org/\1">\2</a>'),

    # switch ftp links to work with http
    (c('<a href="ftp://(?:ftp\.)?(.+?)">(.+?)</a>'), r'<a href="http://\1">\2</a>'),
    (c('<a href="ftp\.(.+?)">(.+?)</a>'), r'<a href="http://\1">\2</a>'),

    # attempt to convert git, ssh and rsync urls into http
    (c('<a href="(?:git|ssh|rsync)://(.+?)">(.+?)</a>'), r'<a href="http://\1">\2</a>'),

    # remove links to domains which generally dont work
    (c(r'<a href="https?://(?:{}).*?">(.+?)</a>'.format('|'.join(INVALID_URLS))), r'\1'),

    # empty links
    (c('<a href="https?://">(.+?)</a>'), r'\1'),

    # include number in internal links link name
    (c('(<a href="/.+?">)(.+?)(</a>(?:</b>)?)(\(\d\))'), r'\1\2\4\3'),

    # remove non http(s) links and add target _blank tp external links
    (c('<a href="(.*?)">(.+?)</a>'), replace_non_http),

    # remove the http(s):// from the link name
    (c('<a href="(http.+?)>https?://(.+?)</a>'), r'<a href="\1>\2</a>'),
]


def man_fix_external_links(content):
    for regex, repl in CHANGE_EXTERNAL_LINKS:
        content = regex.sub(repl, content)
    return content


def check_man_pages():
    """
    Check external link fixing.
    """
    with Path('data/man_metadata.json').open() as f:
        man_data = json.load(f)

    html_root = Path('data/html').resolve()
    print('{} pages to go through'.format(len(man_data)))
    remaining_links = re.compile('<a href="[^/].+?</a>')
    for data in man_data:
        # if data['man_id'] != 1:
        #     continue
        html_path = html_root / 'man' / '{raw_path}.html'.format(**data)
        html_path = html_path.resolve()
        content = html_path.read_text()
        content = man_fix_external_links(content)
        links = remaining_links.findall(content)
        if links:
            print('{}\n    {}'.format(str(html_path)[-30:], '\n    '.join(links)))
            print('')


FIND_LINKS = c(r'https?://[a-zA-Z0-9\.]{3,}.(?:com|net|org|io|uk|fr)\S*')
TAG_ENDING = c('(?:&gt;?|&lt;?|&amp;|&quot;|&#\d{2,};|\)|\.)+$')


def replace_link(m):
    link = m.group()
    ending = ''
    m2 = TAG_ENDING.search(link)
    if m2:
        link = m2.string[:m2.start()]
        ending = m2.group()
    return '<a href="{0}" target="_blank">{1}</a>{2}'.format(unescape(link), link, ending)


def help_fix_external_links(content):
    return FIND_LINKS.sub(replace_link, escape(content))


def check_help_pages():
    with Path('data/exec_data.json').open() as f:
        exec_data = json.load(f)

    # print(help_fix_external_links(exec_data['pdfflip']['help_msg']))

    for name, data in sorted(exec_data.items()):
        if data:  # and name in {'xdvi-xaw', 'rst2odt.py'}
            content = escape(data['help_msg'])
            results = list(FIND_LINKS.finditer(content))
            if results:
                print(name)
                for m in results:
                    print('  ',
                          click.style(repr(replace_link(m)), fg='red'),
                          click.style(repr(m.string[m.start() - 10: m.end() + 10]), fg='blue'))


if __name__ == '__main__':
    # check_man_pages()
    check_help_pages()
