#!/usr/bin/env bash

SHELL_DIR=$(dirname $0)

pushd ${SHELL_DIR}

mkdir -p build
mkdir -p config

if [ -f config/deepracer-model.sh ]; then
    . config/deepracer-model.sh
fi

python3 submit.py

popd
