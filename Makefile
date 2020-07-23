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
	PYTHONPATH="${PYTHONPATH}" ${PY} src/manage.py runserver


.PHONY: migrate
migrate:
	PYTHONPATH="${PYTHONPATH}" ${PY} src/manage.py migrate


.PHONY: migrations
migrations:
	PYTHONPATH="${PYTHONPATH}" ${PY} src/manage.py makemigrations


.PHONY: su
su:
	PYTHONPATH="${PYTHONPATH}" ${PY} src/manage.py createsuperuser


.PHONY: sh
sh:
	PYTHONPATH="${PYTHONPATH}" ${PY} src/manage.py shell


