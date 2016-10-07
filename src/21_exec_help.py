import json
import os
import signal
from pathlib import Path
from subprocess import run, TimeoutExpired, PIPE, Popen

STOP_WORDS = 'unknown', 'doctype'


class ExecHelp:
    def __init__(self):
        self.commands = self.run_bash('compgen -c')
        self.commands = {c for c in self.commands.split('\n') if c}
        for arg in ['builtin', 'keyword']:
            v = self.run_bash('compgen -A ' + arg)
            self.commands -= {c for c in v.split('\n') if c}
        self.commands = sorted(self.commands)
        print('found {} commands'.format(len(self.commands)))
        self.path = Path('exec_data.json')
        self.data = {}
        if self.path.exists():
            with self.path.open() as f:
                self.data = json.load(f)
        self.proc = None
        count = 0
        try:
            for command in self.commands:
                if command in self.data:
                    continue
                self.process_cmd(command)
                count += 1
                if count % 5 == 0:
                    self.write()
        finally:
            self.write()
            print('generated info for {} commands'.format(count))

    def write(self):
        with self.path.open('w') as f:
            json.dump(self.data, f, sort_keys=True, indent=2)

    def process_cmd(self, command):
        print(command)
        help_arg, help_msg, help_returncode = self.try_args(command, '--help', 'help', '-help', '-h')
        if not help_msg:
            self.data[command] = 'no data'
            return
        v_arg, v_msg, v_returncode = self.try_args(command, '--version', '-version', 'version', '-v', allow_short=True)
        self.data[command] = dict(
            help_arg=help_arg,
            help_msg=help_msg,
            help_returncode=help_returncode,
            version_arg=v_arg,
            version_msg=v_msg,
            version_returncode=v_returncode,
        )

    def try_args(self, command, *args, allow_short=False):
        msg, returncode = None, None
        next_best = None
        arg = None
        try_args = []
        for _arg in args:
            try_args += [_arg, _arg.upper()]
        for arg in try_args:
            r = self.run(command, arg)
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

    def run(self, cmd, arg):
        self.proc = None
        signal.signal(signal.SIGALRM, self.kill)
        signal.alarm(1)
        # TODO need a way to force isatty() to return false and still get returncode
        try:
            self.proc = Popen('{} {}'.format(cmd, arg), stdout=PIPE, stderr=PIPE, shell=True,
                              executable='/bin/bash', env=dict(os.environ, DISPLAY=''), universal_newlines=True)
        except OSError:
            return
        except Exception as e:
            raise RuntimeError('unexpected error on "{} {}"'.format(cmd, arg)) from e
        try:
            stdout, stderr = self.proc.communicate(timeout=0.5)
        except TimeoutExpired:
            return
        signal.alarm(0)
        return stdout or stderr, self.proc.returncode

    def run_bash(self, cmd):
        p = run(cmd, executable='/bin/bash', stdout=PIPE, stderr=PIPE,
                shell=True, universal_newlines=True)
        if p.returncode != 0:
            raise RuntimeError('"{}" failed, return code {}\nstderr:{}'.format(cmd, p.returncode, p.stderr))
        return p.stdout

    def kill(self, sig, frame):
        self.proc.kill()
        raise TimeoutExpired


if __name__ == '__main__':
    ExecHelp()
