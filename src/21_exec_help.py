import json
import queue
import shutil
import threading
from pathlib import Path
from subprocess import run, PIPE

THEADS = 4

THIS_DIR = Path(__file__).parent.resolve()


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
        self.queue = None
        self.new_cmds = []
        self.started = 0

        self.executor = str((THIS_DIR / 'findhelp.py').resolve())
        self.json_dir = Path('/tmp/findhelp')
        if self.json_dir.exists():
            shutil.rmtree(str(self.json_dir))

        try:
            self.go()
        finally:
            self.write()
            print('generated info for {} commands'.format(len(self.new_cmds)))

    def write(self):
        with self.path.open('w') as f:
            json.dump(self.data, f, sort_keys=True, indent=2)

    def worker(self):
        while True:
            command = self.queue.get()
            if command is None:
                break
            self.process_cmd(command)
            self.new_cmds.append(command)
            if len(self.new_cmds) % 5 == 0:
                self.write()
            self.queue.task_done()

    def go(self):
        sandpit = Path('/tmp/sandpit')
        if sandpit.exists():
            shutil.rmtree(str(sandpit))

        self.queue = queue.Queue()
        threads = []
        for i in range(THEADS):
            t = threading.Thread(target=self.worker)
            t.start()
            threads.append(t)

        for command in self.commands:
            if command in self.data:
                continue
            self.queue.put(command)
            self.started += 1
            if self.started > 1000:
                break

        self.queue.join()

        for i in range(THEADS):
            self.queue.put(None)
        for t in threads:
            t.join()

    def process_cmd(self, command):
        print(command)
        outpath = self.json_dir / '{}.json'.format(command)
        run(['xterm', '-e', '{} {} {}'.format(self.executor, command, outpath)], check=True)
        if not outpath.exists():
            raise RuntimeError('"{}" does not exist'.format(outpath))
        with outpath.open() as f:
            data = json.load(f)
        self.data[command] = data

    def run_bash(self, cmd):
        p = run(cmd, executable='/bin/bash', stdout=PIPE, stderr=PIPE,
                shell=True, universal_newlines=True)
        if p.returncode != 0:
            raise RuntimeError('"{}" failed, return code {}\nstderr:{}'.format(cmd, p.returncode, p.stderr))
        return p.stdout


if __name__ == '__main__':
    ExecHelp()
