#!/usr/bin/env python3
import re
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from devtools import debug
from tqdm import tqdm


def man_to_ansi(path):
    env = {
        'COLUMNS': '1000',
        'LINES': '100',
        'TERM': 'xterm-256color',
        'LANG': 'en_GB.UTF-8',
    }
    cmd = '/home/samuel/code/man-db/src/man', '-P', 'ul', path
    # cmd = 'script', '-e', '-q', '-c', f'man -P ul {name}', '/dev/null'
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, timeout=2)
    body = p.stdout.replace(b'\r\n', b'\n').decode()
    # Path('file.raw').write_text(body)
    # debug(body[:2000])
    return body


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
{{styles}}
</style>
</head>
<body>
{{html}}
</body>
</html>
"""


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


def nbsp(m):
    start, finish = m.span()
    spaces = finish - start - 2
    b, e = m.groups()
    return b + ('&nbsp;' * spaces) + e


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
word_spaces_word = re.compile(r'(\S) {2,}(\S)')


def rep_spaces(line_):
    m_ = details_section.search(line_)
    if m_:
        c1, c2 = m_.groups()
        return (
            f'  <div class="details">\n'
            f'    <div class="d1">{c1.strip(" ")}</div>\n'
            f'    <div class="d2">{word_spaces_word.sub(nbsp, c2)}</div>\n'
            f'  </div>\n'
        )
    else:
        return f'  {word_spaces_word.sub(nbsp, line_)}\n'


seven_spaces = re.compile(r'^ {7}(.+)')
three_spaces = re.compile(r'^ {3}(.+)')
start_space = re.compile(r'^ +')

repeat_div = re.compile(r'<div>\n(<div class="i\d+">\n.+\n</div>)\n</div>')


def ansi_to_html(ansi):
    lines = []

    def add_line(line_):
        line_ = replace_ansi(line_)

        for indent in range(20, 0, -1):
            regex = re.compile('^ {%s}' % (7 + indent))
            if regex.search(line_):
                lines.append(f'<div class="i{indent}">\n{rep_spaces(regex.sub("", line_))}</div>\n')
                return

        m_ = seven_spaces.search(line_)
        if m_:
            # normal line
            lines.append(f'{rep_spaces(m_.group(1))}')
            return

        m_ = three_spaces.search(line_)
        if m_:
            lines.append(f'<h4>{word_spaces_word.sub(nbsp, m_.group(1))}</h4>\n')
            return

        # line is weird and has non standard indent, could use and h4 here?
        if len(line) >= 975:
            # long first or last line, ignore
            return

        lines.append(f'<div class="dedent">\n{rep_spaces(line_)}</div>\n')

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
                lines.append('<div>\n')
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


def main(path: str, save_path=None):
    ansi = man_to_ansi(path)
    html = ansi_to_html(ansi)
    if not save_path:
        save_path = Path('file.html')
        # make it pretty
        html = pretty_html(html)
    save_path.write_text(html)


def run_all():
    src_path = Path('data/man').resolve()
    dst_path = Path('data/html/man')
    dst_path.mkdir(parents=True, exist_ok=True)
    dst_path = dst_path.resolve()

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
                futures[executor.submit(main, str(path), new_path)] = path
                d_count += 1
            print(f'{dir_path}: loaded {d_count} tasks...')
            man_group += 1

        count = 0
        for future in tqdm(as_completed(futures), total=len(futures)):
            path = futures[future]
            try:
                future.result()
            except Exception as e:
                raise RuntimeError(f'error in {path}') from e
            else:
                count += 1
                # print(count, path)

    print(f'===\nTotal {count} generated files')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        file_path = Path(sys.argv[1])
        main(file_path)
    else:
        run_all()
