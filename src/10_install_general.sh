#!/usr/bin/env bash
# modified from https://github.com/samuelcolvin/init-desktop
set -x
# git
sudo apt-add-repository ppa:git-core/ppa -y
# atom
sudo apt-add-repository ppa:webupd8team/atom -y
# pycharm
sudo apt-add-repository ppa:mystic-mirage/pycharm -y
# python versions
sudo add-apt-repository ppa:fkrull/deadsnakes -y
# wine
sudo add-apt-repository ppa:ubuntu-wine/ppa -y

sudo apt-get update
sudo apt-get upgrade -y

sudo apt-get install -y ubuntu-desktop

sudo apt-get install -y g++ gcc build-essential libbz2-dev libssl-dev libreadline-dev libsqlite3-dev tk-dev
sudo apt-get install -y libpng-dev libfreetype6-dev

sudo apt-get install -y python2.5 python2.6 python 2.7 python3.3 python 3.4 python3.5 python3.6

# from above
sudo apt-get install -y git atom pycharm

# general
sudo apt-get install -y vim chromium-browser unzip gparted synaptic landscape-common gdebi curl whois
# python
sudo apt-get install -y python3-pip libpython3-dev python3-dev

# postgresql
sudo apt-get install -y postgresql-client postgresql postgresql-contrib postgresql-server-dev-all
# redis
sudo apt-get install -y redis-server
# general libs
sudo apt-get install -y libjpeg-dev libfreetype6-dev libffi-dev libsqlite3-dev
# recommended by pyenv
sudo apt-get install -y llvm libncurses5-dev libncursesw5-dev

# compiz
sudo apt-get install -y compizconfig-settings-manager compiz-plugins compiz-plugins-extra unity-tweak-tool

# wine
sudo apt-get install -y wine1.8 winetricks

# useful and required for 12_install_popular
python3.6 -m pip install -U pip setuptools virtualenv ipython requests

sudo apt-get upgrade -y
