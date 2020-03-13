#!/usr/bin/env bash

OS_NAME="$(uname | awk '{print tolower($0)}')"

SHELL_DIR=$(dirname $0)

export PROFILE=$1
export MODEL=$2

_load() {
    URL=$1
    if [ "${URL}" == "" ]; then
        return
    fi

    echo "_load ${URL}"

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

_load_profile() {
    # PROFILE
    if [ -z "${PROFILE}" ]; then
        if [ "${PROFILE_URL}" != "" ]; then
            _load "${PROFILE_URL}"

            export PROFILE="${SELECTED:-$PROFILE}"
        fi
    fi

    echo "PROFILE: ${PROFILE}"

    if [ -z "${PROFILE}" ]; then
        exit 1
    fi

    if [ -f config/${PROFILE}.sh ]; then
        echo "load config/${PROFILE}.sh"
        source config/${PROFILE}.sh
    fi
}

_load_model() {
    # MODEL
    if [ -z "${MODEL}" ]; then
        if [ "${MODEL_URL}" != "" ]; then
            _load "${MODEL_URL}"

            export MODEL="${SELECTED:-$MODEL}"
        fi
    fi

    echo "MODEL: ${MODEL}"

    if [ -z "${MODEL}" ]; then
        exit 1
    fi
}

pushd ${SHELL_DIR}

git pull

mkdir -p build
mkdir -p config

if [ -f config/deepracer-model.sh ]; then
    source config/deepracer-model.sh
fi

_load_profile

_load_model

# submit
python3 submit.py

popd
