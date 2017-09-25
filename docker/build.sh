#!/usr/bin/env bash

set -e

THIS_DIR=`dirname "$0"`

cd ${THIS_DIR}
if [[ ! -d tmp ]]; then
    echo "creating tmp directory..."
    mkdir tmp
else
    echo "tmp directory already exists"
fi

echo "copying necessary files into place..."
rsync -i -a Dockerfile tmp/
# required to avoid interactive prompt
rsync -i -a /etc/default/keyboard tmp/

echo "building docker image..."
docker build tmp -t hm
echo "done."
