#!/bin/bash

export PYTHONPATH=.
export PYTHONUNBUFFERED=TRUE
CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

${CURR_DIR}/wait-for-it.sh ${DATABASE_HOST} ${DATABASE_PORT}
${CURR_DIR}/wait-for-it.sh ${ELASTIC_DOMAIN} ${ELASTIC_PROT}
${CURR_DIR}/wait-for-it.sh ${RABBIT_MQ_HOST} ${RABBIT_MQ_PORT}
python3 consumer/main.py