#! /usr/bin/python3.6
import json
import os
import signal
import sys
from itertools import chain
from pathlib import Path
from subprocess import TimeoutExpired, PIPE, Popen

import chardet

STOP_WORDS = 'unknown', 'doctype'


def process_cmd(command):
    sandpit = Path('/tmp/sandpit')
    sandpit.mkdir(parents=True, exist_ok=True)
    os.chdir(str(sandpit))
    help_arg, help_msg, help_returncode = try_args(command, check_help, '--help', 'help', '-help', '-h', '')
    v_arg, v_msg, v_returncode = try_args(command, check_version, '--version', '-version', 'version', '-v')
    if not help_msg and not v_msg:
        print('no help message or version message found', command)
        return None

    print('help and version messages found', command)
    return dict(
        name=command,
        help_arg=help_arg,
        help_msg=help_msg,
        help_returncode=help_returncode,
        version_arg=v_arg,
        version_msg=v_msg,
        version_returncode=v_returncode,
    )


def check_help(rc, output):
    start = output[:150].lower()

    if any(sw in start for sw in STOP_WORDS):
        return False

    if rc == 0 or 'usage' in start:
        return True

    if len(output) < 80:
        return False


def check_version(rc, output):
    start = output[:150].lower()

    if any(sw in start for sw in STOP_WORDS):
        return False

    if rc == 0:
        return True


def try_args(command, callback, *args):
    msg, returncode = None, None
    next_best = None
    arg = None
    try_args = [(_arg, _arg.upper()) for _arg in args]
    for arg in chain(*try_args):
        r = run(command, arg)
        if r is None:
            continue
        out, rc = r
        result = callback(rc, out)

        if result is False:
            continue
        elif result is True:
            returncode = rc
            msg = out
            break

        if out and next_best is None:
            next_best = out, rc
    if not msg and next_best:
        msg, returncode = next_best
    return arg, msg, returncode


def decode(s, encoding='utf8', retry=0):
    try:
        return s.decode(encoding)
    except UnicodeDecodeError:
        alt_encoding = chardet.detect(s)['encoding']
        if retry < 3 and alt_encoding:
            return decode(s, alt_encoding, retry + 1)
        return None


def run(cmd, arg):
    try:
        proc = Popen(
            '{} {}'.format(cmd, arg).strip(' '),
            stdout=PIPE,
            stderr=PIPE,
            executable='/bin/bash',
            shell=True,
            env=dict(os.environ, DISPLAY=''),
        )
    except OSError:
        return
    except Exception as e:
        raise RuntimeError('unexpected error on "{} {}"'.format(cmd, arg)) from e

    def kill(sig, frame):
        proc.kill()
        raise TimeoutExpired

    signal.signal(signal.SIGALRM, kill)
    signal.alarm(1)
    try:
        stdout, stderr = proc.communicate(timeout=0.5)
    except TimeoutExpired:
        return
    signal.alarm(0)
    out = decode(stdout or stderr)
    if out is None:
        return
    return out, proc.returncode


if __name__ == '__main__':
    command, outpath = sys.argv[-2], sys.argv[-1]
    outpath = Path(outpath)
    if not outpath.exists():
        data = process_cmd(command)
        outpath.parent.mkdir(parents=True, exist_ok=True)
        with outpath.open('w') as f:
            json.dump(data, f, sort_keys=True, indent=2)
