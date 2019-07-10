#!/usr/bin/env bash

SHELL_DIR=$(dirname $0)

pushd ${SHELL_DIR}

mkdir -p build

pytest submit.py

popd
