#!/usr/bin/env bash

OS_NAME="$(uname | awk '{print tolower($0)}')"

SHELL_DIR=$(dirname $0)

export LEAGUE=$1
export SEASON=$2
export MODEL=$3

_echo() {
    if [ "${TPUT}" != "" ] && [ "$2" != "" ]; then
        echo -e "$(tput setaf $2)$1$(tput sgr0)"
    else
        echo -e "$1"
    fi
}

_result() {
    _echo "# $@" 4
}

_command() {
    _echo "$ $@" 3
}

_success() {
    _echo "+ $@" 2
    exit 0
}

_error() {
    _echo "- $@" 1
    exit 0
}

_init() {
    mkdir -p build
    mkdir -p config

    if [ -f config/deepracer.sh ]; then
        source config/deepracer.sh
    fi
}

_select_one() {
    COUNT=$(cat ${LIST} | wc -l | xargs)

    SELECTED=

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
        SELECTED=$(sed -n ${RND}p ${LIST} | cut -d' ' -f1)
    fi
}

_load_season() {
    echo "LEAGUE: ${LEAGUE}"

    if [ -z "${LEAGUE}" ]; then
        _error "Not set LEAGUE"
    fi

    if [ -f config/${LEAGUE}.sh ]; then
        echo "load config/${LEAGUE}.sh"
        source config/${LEAGUE}.sh
    fi

    if [ -z "${SEASON}" ]; then
        LIST=build/season.txt

        curl -sL ${LEAGUE_URL} \
            | jq -r --arg LEAGUE "${LEAGUE}" '.[] | select(.league==$LEAGUE) | "\(.season)"' \
            > ${LIST}

        _select_one

        export SEASON="${SELECTED}"
    fi

    echo "SEASON: ${SEASON}"

    if [ -z "${SEASON}" ]; then
        _error "Not set SEASON"
    fi
}

_load_models() {
    if [ -z "${MODEL}" ]; then
        LIST=build/models.txt

        curl -sL ${LEAGUE_URL} \
            | jq -r --arg LEAGUE "${LEAGUE}" '.[] | select(.league==$LEAGUE) | "\(.models[].name)"' \
            > ${LIST}

        _select_one

        export MODEL="${SELECTED}"
    fi

    echo "MODEL: ${MODEL}"

    if [ -z "${MODEL}" ]; then
        _error "Not set MODEL"
    fi
}

_run() {
    pushd ${SHELL_DIR}

    _init

    _load_season

    _load_models

    # submit
    python3 submit.py -l ${LEAGUE} -s ${SEASON} -m ${MODEL}

    popd
}

_run
