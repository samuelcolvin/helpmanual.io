#! /usr/bin/python3.5
import json
import os
import signal
import sys
from itertools import chain
from pathlib import Path
from subprocess import TimeoutExpired, PIPE, Popen

STOP_WORDS = 'unknown', 'doctype'


def process_cmd(command):
    help_arg, help_msg, help_returncode = try_args(command, '--help', 'help', '-help', '-h')
    if not help_msg:
        return None
    v_arg, v_msg, v_returncode = try_args(command, '--version', '-version', 'version', '-v', allow_short=True)
    return dict(
        command=command,
        help_arg=help_arg,
        help_msg=help_msg,
        help_returncode=help_returncode,
        version_arg=v_arg,
        version_msg=v_msg,
        version_returncode=v_returncode,
    )


def try_args(command, *args, allow_short=False):
    msg, returncode = None, None
    next_best = None
    arg = None
    try_args = [(_arg, _arg.upper()) for _arg in args]
    for arg in chain(*try_args):
        r = run(command, arg)
        if r is None:
            continue
        out, rc = r
        start = out[:150].lower()

        if any(sw in start for sw in STOP_WORDS):
            continue

        if not allow_short and len(out) < 150:
            continue

        if rc == 0 or 'usage' in start:
            returncode = rc
            msg = out
            break

        if out and next_best is None:
            next_best = out, rc
    if not msg and next_best:
        msg, returncode = next_best
    return arg, msg, returncode


def run(cmd, arg):
    try:
        proc = Popen(
            '{} {}'.format(cmd, arg),
            stdout=PIPE,
            stderr=PIPE,
            executable='/bin/bash',
            shell=True,
            universal_newlines=True,
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
    return stdout or stderr, proc.returncode


if __name__ == '__main__':
    command, outpath = sys.argv[-2], sys.argv[-1]
    outpath = Path(outpath)
    if not outpath.exists():
        sandpit = Path('/tmp/sandpit')
        sandpit.mkdir(parents=True, exist_ok=True)
        os.chdir(str(sandpit))
        data = process_cmd(command)
        outpath.parent.mkdir(parents=True, exist_ok=True)
        with outpath.open('w') as f:
            json.dump(data, f, sort_keys=True, indent=2)
