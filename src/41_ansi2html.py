#!/usr/bin/env python3
import json
import re
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from devtools import debug
from tqdm import tqdm


html_escapes = {'&': '&amp;', '<': '&lt;', '>': '&gt;'}
template = """
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title></title>
<style>
body {
  word-wrap: break-word;
  font-family: 'Ubuntu Mono', monospace;
  color: #d3d7cf;
  background-color: #232627;
  margin-left: 4rem;
}
div {
  margin: 0 0 1rem 0;
  white-space: pre-wrap;
}
.dedent {
  margin-left: -3.5rem;
  display: block
}
.inv_foreground { color: #000000; }
.inv_background { background-color: #AAAAAA; }
h3, h4 {
  padding: 0;
  margin: 0 0 0 -3.5rem;
  line-height: 1;
  font-size: 1.1rem;
}
h4 {
  font-size: 1rem;
  font-weight: 700;
  margin-left: -2rem;
}
.table-line {
  color: #4fc3f7
}
.details {
  display: flex;
  justify-content: flex-start;
  margin-left: 0;
}
.details > div {
  margin: 0;
}
.details .d1 { 
  width: 3.5rem;
  flex-shrink: 0;
}
i {
  font-weight: 700;
  text-decoration: underline;
  font-style: normal;
}
a {
  color: #48aaff;
}
{{styles}}
</style>
</head>
<body>
{{html}}
</body>
</html>
"""

link_regex = re.compile(r'(https?://\S+|www\.\S+)')
other_man_regexes = [
    re.compile(r'([a-zA-Z]{2,}) ?\((\d)\)'),
    re.compile(r'<u>([a-zA-Z]{2,})</u> ?\((\d)\)'),
    re.compile(r'<b>([a-zA-Z]{2,})</b> ?\((\d)\)'),
    re.compile(r'<i>([a-zA-Z]{2,})</i> ?\((\d)\)'),
]
include_h_regex = re.compile(r'&lt;(([a-zA-Z]{2,})\.h)&gt;')

INVALID_URLS = {
    r'pastebin',
    r'localhost',
    r'example.',
    r'www.example',
    r'site.com',
    r'www.site.com',
    r'host.',
    r'HOST',
    r'USER@HOST',
    r'foo.com',
    r'foo.bar',
    r'bar.com',
    r'api.github.com',
}


def replace_link(m):
    link = m.group(0)
    if any(url in link for url in INVALID_URLS):
        return link
    if not link.startswith('http'):
        link = 'http://' + link
    return f'<a href="{link}" target="_blank">{m.group(0)}</a>'


# currently has to be global

with Path('data/man_metadata.json').open() as f:
    man_data = json.load(f)
man_uris = {d['uri'] for d in man_data}


def find_links(html, this_uri):
    html = link_regex.sub(replace_link, html)
    missing = Counter()

    def replace_other_man(m):
        name, group = m.groups()
        group = int(group)

        # special case:
        if (name, group) == ('ImageMagick', 1):
            return f'<a href="/man1/convert">ImageMagick(1)</a>'

        groups = [group] + [g for g in range(1, 10) if g != group]
        for suffix in ['', '-ssl', '-tcl']:
            for g in groups:
                if name == 'ImageMagick':
                    uri = f'/man{g}/convert'
                else:
                    uri = f'/man{g}/{name}{suffix}'
                if uri != this_uri and uri in man_uris:
                    return f'<a href="{uri}">{name}({g})</a>'

        if group == 1:
            # don't care about other missing packages
            missing[name] += 1
            # missing[f'{name}({group})'] += 1
        return m.group(0)

    for regex in other_man_regexes:
        html = regex.sub(replace_other_man, html)

    def replace_include_h(m):
        name = m.group(2).replace('/', '_')
        inc_uris = [
            f'/man3/{name}.h',
            f'/man2/{name}.h',
            f'/man7/{name}.h',
            f'/man7/{name}.h-posix',
            f'/man3/{name}',
            f'/man2/{name}',
            f'/man7/{name}',
            f'/man7/{name}-posix',
            f'/man2/{name[4:]}'
        ]

        try:
            link = next(v for v in inc_uris if v in man_uris)
        except StopIteration:
            # missing[f'{name}(?)'] += 1
            return m.group(0)
        else:
            return f'&lt;<a href="{link}">{m.group(1)}</a>&gt;'

    html = include_h_regex.sub(replace_include_h, html)
    return html, missing


ansi_re = re.compile(r'\x1b\[(?:\d|;)*[a-zA-Z]')
heading = re.compile(r'^\x1b\[1m(.+)\x1b\[0m')
table_border = re.compile('([┌┬┐└┴┘├┼┤─│]+)')
underline_space = re.compile('<u>[^<]*? [^<]*?</u>')
spaces = re.compile('( +)')

regexes = [
    (re.compile(r'\x1b\[1m(.+?)\x1b\[0m'), r'<b>\1</b>'),
    (re.compile(r'\x1b\[4m(.+?)\x1b\[24m'), r'<u>\1</u>'),
    (re.compile(r'\x1b\[7m(.+?)\x1b\[0m'), r'<i>\1</i>'),
    (re.compile(r'</([bu])>( *)<\1>'), r'\2'),
]


def strip_ansi(value):
    return ansi_re.sub('', value)


def replace_ansi(line):
    for pattern, special in html_escapes.items():
        line = line.replace(pattern, special)
    for regex, rep in regexes:
        line = regex.sub(rep, line)

    # convert table borders to a funky colour, will this mess up with just pipe operators?
    line = table_border.sub(r'<span class="table-line">\1</span>', line)

    # spaces shouldn't be underlined
    line = underline_space.sub(lambda m: spaces.sub(r'</u>\1<u>', m.group(0)), line)
    return line


details_section = re.compile(r'^(\S.{4}) {2}(\S.+)')


def rep_spaces(line_):
    m_ = details_section.search(line_)
    if m_:
        c1, c2 = m_.groups()
        return (
            f'<div class="details">'
            f'<div class="d1">{c1.strip(" ")}</div>'
            f'<div class="d2">{c2}</div>'
            f'</div>'
        )
    else:
        return f'{line_}\n'


seven_spaces = re.compile(r'^ {7}(.+)')
three_spaces = re.compile(r'^ {3}(.+)')
start_space = re.compile(r'^ +')

repeat_div = re.compile(r'<div>(<div class="i\d+">.+</div>)</div>')


def ansi_to_html(ansi: str):
    lines = []

    def add_line(line_):
        line_ = replace_ansi(line_)

        for indent in range(20, 0, -1):
            regex = re.compile('^ {%s}' % (7 + indent))
            if regex.search(line_):
                lines.append(f'<div class="i{indent}">{rep_spaces(regex.sub("", line_))}</div>')
                return

        m_ = seven_spaces.search(line_)
        if m_:
            # normal line
            lines.append(f'{rep_spaces(m_.group(1))}')
            return

        m_ = three_spaces.search(line_)
        if m_:
            lines.append(f'<h4>{m_.group(1)}</h4>\n')
            return

        # line is weird and has non standard indent, could use and h4 here?
        if len(line) >= 975:
            # long first or last line, ignore
            return

        lines.append(f'<div class="dedent">{rep_spaces(line_)}</div>\n')

    in_para = False
    in_section = False
    for line in ansi.split('\n')[1:-2]:
        if heading.search(line):
            if in_para:
                lines.append('</div>\n')
                in_para = False
            if in_section:
                lines.append('</section>\n\n')
            h = heading.sub(r'\1', line)
            lines.append(f'<h3>{strip_ansi(h)}</h3>\n<section>\n')
            in_section = True
        elif line == '':
            if in_para:
                lines.append('</div>\n')
                in_para = False
        else:
            if not in_para:
                lines.append('<div>')
                in_para = True
            add_line(line)

    if in_section:
        lines.append('</section>\n')
    html = ''.join(lines)
    html = repeat_div.sub(r'\1', html)

    m = ansi_re.search(html)
    if m:
        debug(html[m.start() - 100:m.end() + 100])
        raise RuntimeError('ansi strings found in html')
    return html


def pretty_html(html):
    html = template.replace('{{html}}', html)
    styles = '\n'.join(f'.i{v} {{margin-left: {v / 2:0.1f}rem;}}\n' for v in range(1, 21))
    return html.replace('{{styles}}', styles)


def main(path: Path, save_path: Path = None, this_uri: str = '<missing>'):
    ansi = path.read_text()
    html = ansi_to_html(ansi)
    html, missing_links = find_links(html, this_uri)
    if not save_path:
        save_path = Path('file.html')
        # make it pretty
        html = pretty_html(html)
    save_path.write_text(html)
    return missing_links


def run_all():
    src_path = Path('data/ansi').resolve()
    dst_path = Path('data/html/man')
    dst_path.mkdir(parents=True, exist_ok=True)
    dst_path = dst_path.resolve()

    count = 0
    missing = Counter()
    man_group = 1
    with ProcessPoolExecutor(max_workers=12) as executor:
        futures = {}
        while True:
            dir_path = src_path / f'man{man_group}'
            if not dir_path.exists():
                break

            d_count = 0
            for path in dir_path.iterdir():
                new_path = dst_path / path.relative_to(src_path).with_suffix('{}.html'.format(path.suffix))
                this_uri = f'/man{man_group}/{path.name}'
                futures[executor.submit(main, path, new_path, this_uri)] = path
                d_count += 1
            print(f'{dir_path}: loaded {d_count} tasks...')
            man_group += 1

        for future in tqdm(as_completed(futures), total=len(futures)):
            path = futures[future]
            try:
                missing_ = future.result()
            except Exception as e:
                raise RuntimeError(f'error in {path}') from e
            else:
                missing.update(missing_)
                count += 1
                # print(count, path)

    print(f'===\nTotal {count} generated files')
    print('most common missing links:')
    for name, count in sorted(missing.items(), key=lambda i: i[1], reverse=True)[:200]:
        print(f'{name:>25}: {count}')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        file_path = Path(sys.argv[1])
        main(file_path)
    else:
        run_all()
