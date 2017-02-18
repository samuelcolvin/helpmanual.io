#!/usr/bin/env python3.6
import subprocess

import requests

URL = 'http://popcon.ubuntu.com/by_inst'
PACKAGES_1K =  'bytes=0-110000'
PACKAGES_5K =  'bytes=0-550000'
PACKAGES_30K = 'bytes=0-3300000'


def install_packages(*packages):
    commands = ('sudo', 'apt-get', 'install', '-y') + packages
    print('installing: {}'.format(commands))
    subprocess.run(commands)


def install_popular():
    r = requests.get(URL, headers={'Range': PACKAGES_5K})
    print('downloaded {}, status: {}'.format(URL, r.status_code))
    assert 200 <= r.status_code < 300
    text = r.text
    print('size: {:0.2f}kb'.format(len(text)/1024))
    packages = []
    for line in text.split('\n')[:-1]:
        if line.startswith('#'):
            continue
        parts = line.split()
        packages.append(parts[1])
    print('{} packages to install'.format(len(packages)))
    step = 100
    finished = False
    i_b4 = 0
    for i in range(step, 100000, step):
        if i >= len(packages):
            i = len(packages) - 1
            finished = True
        start = max(i_b4, i - step)
        print('\n\n\n\n# packages: {} - {}\n'.format(start, i))
        install_packages(*packages[start:i])
        i_b4 = i
        if finished:
            break

if __name__ == '__main__':
    install_popular()
