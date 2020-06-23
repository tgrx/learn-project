HERE := $(shell pwd)
VENV := $(shell pipenv --venv)
SRC := ${HERE}/src
PYTHONPATH := ${SRC}

RUN := pipenv run
PY := ${RUN} python


.PHONY: format
format:
	${RUN} isort --virtual-env "${VENV}" --recursive --apply "${HERE}"
	${RUN} black "${HERE}"


.PHONY: run
run:
	PYTHONPATH="${PYTHONPATH}" ${PY} -m srv
