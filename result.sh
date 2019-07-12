#!/usr/bin/env bash

# An error occurred (InvalidParameterException) when calling the StartQuery operation:
# Log group '/aws/deepracer/leaderboard/SimulationJobs' does not exist for account ID '00000'
# (Service: AWSLogs; Status Code: 400; Error Code: InvalidParameterException; Request ID: xxx-000-000-000-xxx)

OS_NAME="$(uname | awk '{print tolower($0)}')"

SHELL_DIR=$(dirname $0)

START_TIME=
END_TIME=

if [ "${OS_NAME}" == "darwin" ]; then
    START_TIME="$(date -v -15M "+%s")"
    END_TIME="$(date "+%s")"
else
    START_TIME="$(date -v -15M "+%s")"
    END_TIME="$(date "+%s")"
fi

LOG_GROUP="/aws/deepracer/leaderboard/SimulationJobs"

QUERY="fields @message | filter @message =~ 'SIM_TRACE_LOG' and @message =~ '0,True' | order by @timestamp desc, @message desc"

aws logs start-query \
    --log-group-name "${LOG_GROUP}" \
    --start-time ${START_TIME} \
    --end-time ${END_TIME} \
    --query-string "${QUERY}"
