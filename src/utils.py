import subprocess
from pathlib import Path


def man_to_txt(p: Path):
    p = subprocess.Popen(['man', str(p)], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         env={'COLUMNS': '10000'}, universal_newlines=True)
    stdout, stderr = p.communicate(timeout=2)
    if p.returncode:
        raise RuntimeError('man failed: return code {}\nstderr:{}'.format(p.returncode, stderr))
    return stdout


def txt_to_html(man_txt: str):
    lines = man_txt.split('\n')[1:]
    html_lines = []
    for line in lines:
        if not line:
            continue
        if line.startswith(' ' * 10):
            html_lines.append('<p class="indented">{}</p>'.format(line.strip(' ')))
        elif line.startswith(' ' * 5):
            html_lines.append('<p>{}</p>'.format(line.strip(' ')))
        else:
            html_lines.append('<h2>{}</h2>'.format(line))
    return '\n'.join(html_lines).strip('\n')
