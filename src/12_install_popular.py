#!/usr/bin/env python3.6
import subprocess

import requests
from tqdm import tqdm

URL = 'http://popcon.ubuntu.com/by_inst'
PACKAGES_1K =  'bytes=0-110000'
PACKAGES_10K = 'bytes=0-1100000'
PACKAGES_30K = 'bytes=0-3300000'


def install_popular():
    r = subprocess.run(('apt', 'list', '--installed'), stdout=subprocess.PIPE)
    existing_packages = r.stdout.decode().split('\n')[1:]
    existing_packages = {p.split('/', 1)[0] for p in existing_packages}
    r = requests.get(URL, headers={'Range': PACKAGES_10K})
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
    for package in tqdm(packages):
        if package in existing_packages:
            continue
        subprocess.run(('sudo', 'apt-get', 'install', '-y', package))

if __name__ == '__main__':
    install_popular()
