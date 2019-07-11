#!/usr/bin/env bash

SHELL_DIR=$(dirname $0)

pushd ${SHELL_DIR}

git pull

mkdir -p build
mkdir -p config

if [ -f config/deepracer-model.sh ]; then
    . config/deepracer-model.sh
fi

if [ "${MODEL_URL}" != "" ]; then
    export MODEL="$(curl -sL ${MODEL_URL} | xargs)"
fi

python3 submit.py

popd
