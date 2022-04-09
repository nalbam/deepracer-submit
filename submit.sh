#!/usr/bin/env bash

OS_NAME="$(uname | awk '{print tolower($0)}')"

SHELL_DIR=$(dirname $0)

export DR_TARGET=$1

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
        SELECTED=$(sed -n ${RND}p ${LIST})
    fi
}

_load_season() {
    echo "DR_TARGET: ${DR_TARGET}"

    if [ -z ${DR_TARGET} ]; then
        _error "Not set DR_TARGET"
    fi

    if [ -f config/${DR_TARGET}.sh ]; then
        echo "load config/${DR_TARGET}.sh"
        source config/${DR_TARGET}.sh
    fi

    if [ -z ${DR_SEASON} ]; then
        LIST=build/season.txt

        curl -sL ${DR_TARGET_URL} \
            | jq -r --arg DR_TARGET "${DR_TARGET}" '.[] | select(.target==$DR_TARGET) | "\(.enable) \(.arn) \(.league) \(.season)"' \
            > ${LIST}

        _select_one

        ARR=(${SELECTED})

        if [ "${ARR[0]}" == "false" ]; then
            _error "Not enabled"
        fi

        export DR_ARN="${ARR[1]}"
        export DR_LEAGUE="${ARR[2]}"
        export DR_SEASON="${ARR[3]}"
    fi

    echo "DR_LEAGUE: ${DR_LEAGUE}"
    echo "DR_SEASON: ${DR_SEASON}"

    if [ -z ${DR_SEASON} ]; then
        _error "Not set DR_SEASON"
    fi
}

_load_models() {
    if [ -z ${DR_MODEL} ]; then
        LIST=build/models.txt

        curl -sL ${DR_TARGET_URL} \
            | jq -r --arg DR_TARGET "${DR_TARGET}" '.[] | select(.target==$DR_TARGET) | "\(.models[].name)"' \
            > ${LIST}

        _select_one

        export DR_MODEL="${SELECTED}"
    fi

    echo "DR_MODEL: ${DR_MODEL}"

    if [ -z ${DR_MODEL} ]; then
        _error "Not set DR_MODEL"
    fi
}

_submit() {
    pushd ${SHELL_DIR}

    _init

    _load_season

    _load_models

    # submit
    _command "submit.py ${DR_ARN} ${DR_TARGET} ${DR_LEAGUE} ${DR_SEASON} ${DR_MODEL}"
    python3 submit.py -a "${DR_ARN}" -t "${DR_TARGET}" -l "${DR_LEAGUE}" -s "${DR_SEASON}" -m "${DR_MODEL}"

    popd
}

_result() {
    pushd ${SHELL_DIR}

    _init

    _load_season

    # result
    _command "result.py ${DR_ARN} ${DR_TARGET} ${DR_LEAGUE} ${DR_SEASON}"
    python3 result.py -a "${DR_ARN}" -t "${DR_TARGET}" -l "${DR_LEAGUE}" -s "${DR_SEASON}"

    popd
}

_submit
