#!/bin/bash

export PYTHONPATH=.
export PYTHONUNBUFFERED=TRUE
alembic upgrade head

UVICORN_COMMAND="uvicorn app.main:app --no-access-log --proxy-headers --host 0.0.0.0 --port 8000"
exec ${UVICORN_COMMAND} --reload