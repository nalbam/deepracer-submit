#!/usr/bin/env bash

SHELL_DIR=$(dirname $0)

pushd ${SHELL_DIR}

git pull

mkdir -p build
mkdir -p config

if [ -f config/deepracer-model.sh ]; then
    . config/deepracer-model.sh
fi

if [ "${model_url}" != "" ]; then
    export model="$(curl -sL ${model_url} | xargs)"
fi

python3 submit.py

popd
