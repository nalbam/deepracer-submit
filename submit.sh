#!/usr/bin/env bash

OS_NAME="$(uname | awk '{print tolower($0)}')"

SHELL_DIR=$(dirname $0)

pushd ${SHELL_DIR}

git pull

mkdir -p build
mkdir -p config

if [ -f config/deepracer-model.sh ]; then
    . config/deepracer-model.sh
fi

if [ "${MODEL_URL}" != "" ]; then
    # export MODEL="$(curl -sL ${MODEL_URL} | xargs)"

    MODELS=config/models.txt

    curl -sL ${MODEL_URL} > ${MODELS}

    COUNT=$(cat ${MODELS} | wc -l | xargs)

    # random
    if [ "${COUNT}" -gt 1 ]; then
        if [ "${OS_NAME}" == "darwin" ]; then
            RND=$(ruby -e "p rand(1...${COUNT})")
        else
            RND=$(shuf -i 1-${COUNT} -n 1)
        fi
    else
        RND=1
    fi

    echo "${RND} / ${COUNT}"

    # get one
    if [ ! -z ${RND} ]; then
        export MODEL=$(sed -n ${RND}p ${MODELS})
    fi
fi

echo "MODEL: ${MODEL}"

python3 submit.py

popd
