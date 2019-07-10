#!/usr/bin/env bash

SHELL_DIR=$(dirname $0)

pushd ${SHELL_DIR}

mkdir -p build

python3 submit.py

popd
