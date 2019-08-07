#!/usr/bin/env bash

OS_NAME="$(uname | awk '{print tolower($0)}')"

SHELL_DIR=$(dirname $0)

pushd ${SHELL_DIR}

git pull

mkdir -p build
mkdir -p config

if [ -f config/deepracer-model.sh ]; then
    source config/deepracer-model.sh
fi

_load() {
    URL=$1

    SELECTED=

    TMP=build/temp.txt

    curl -sL ${URL} > ${TMP}

    COUNT=$(cat ${TMP} | wc -l | xargs)

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

    if [ ! -z ${RND} ]; then
        SELECTED=$(sed -n ${RND}p ${TMP})
    fi
}

# PROFILE
_load "${PROFILE_URL}"

echo "PROFILE: ${SELECTED}"

if [ "${SELECTED}" != "" ] && [ -f config/${SELECTED}.sh ]; then
    export PROFILE="${SELECTED}"

    source config/${SELECTED}.sh
fi

# MODEL
_load "${MODEL_URL}"

echo "MODEL: ${SELECTED}"

if [ "${SELECTED}" != "" ]; then
    export MODEL="${SELECTED}"
fi

# submit
python3 submit.py

popd
