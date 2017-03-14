#!/usr/bin/env python3.6
import json
import shlex
import subprocess
from pathlib import Path

DATA_DIR = (Path(__file__).parent / '../data').resolve()


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


def generate_description(first_line: str, extra: list=None):
    first_line = first_line.strip(' ')
    full = True
    try:
        s_end = first_line.index('.')
        assert s_end > 20
    except (ValueError, AssertionError):
        s_end = len(first_line)
        if s_end < 20 and extra:
            new_line = first_line + ' ' + ' '.join(l.strip(' ') for l in extra if l.strip(' '))
            return generate_description(new_line)

    if s_end > 140:
        full = False
        s_end = 137
        while first_line[s_end] != ' ':
            s_end -= 1
    description = first_line[:s_end]
    if not full:
        description += '...'
    return description


class UniversalEncoder(json.JSONEncoder):
    ENCODER_BY_TYPE = {
        set: list,
        frozenset: list,
        bytes: lambda o: o.decode(),
    }

    def default(self, obj):
        encoder = self.ENCODER_BY_TYPE[type(obj)]
        return encoder(obj)


def run(cmd):
    p = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if p.returncode != 0:
        raise RuntimeError(f'"{cmd}" failed, return code {p.returncode}\nstdout:{p.stdout}\nstderr:{p.stderr}')
    return p.stdout


def run_bash(cmd) -> str:
    p = subprocess.run(cmd, executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       shell=True, universal_newlines=True)
    if p.returncode != 0:
        raise RuntimeError('"{}" failed, return code {}\nstderr:{}'.format(cmd, p.returncode, p.stderr))
    return p.stdout
