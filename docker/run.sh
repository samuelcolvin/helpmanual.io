#!/usr/bin/env bash

set -e
docker run -it --rm -v `pwd`/src:/home/root/src -v `pwd`/data:/home/root/data hm:3 $@
