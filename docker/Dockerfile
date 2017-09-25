FROM ubuntu:17.10

LABEL maintainer "s@muelcolvin.com"

RUN apt-get update

RUN apt-get install -y apt-utils software-properties-common python-software-properties

RUN apt-add-repository ppa:git-core/ppa -y \
 && apt-get update

RUN apt-get upgrade -y

ENV DEBIAN_FRONTEND noninteractive
ADD ./keyboard /etc/default/keyboard

RUN apt-get install -y ubuntu-desktop

RUN apt-get install -y g++ gcc build-essential libbz2-dev libssl-dev libreadline-dev libsqlite3-dev tk-dev
RUN apt-get install -y libpng-dev libfreetype6-dev
RUN apt-get install -y python3.6 python3.6-dev python3.7 python3.7-dev
RUN apt-get install -y python3-pip libpython3-dev
RUN apt-get install -y vim chromium-browser unzip gparted synaptic landscape-common gdebi curl whois
RUN apt-get install -y postgresql-client postgresql postgresql-contrib postgresql-server-dev-all
RUN apt-get install -y redis-server
RUN apt-get install -y libjpeg-dev libfreetype6-dev libffi-dev libsqlite3-dev
RUN apt-get install -y llvm libncurses5-dev libncursesw5-dev
RUN apt-get install -y git
RUN apt-get upgrade -y

RUN python3.6 -m pip install -U pip setuptools virtualenv ipython requests tqdm click

WORKDIR /home/root
