HERE := $(shell pwd)
VENV := $(shell pipenv --venv)
SRC := ${HERE}/src
PYTHONPATH := ${SRC}

RUN := pipenv run
PY := ${RUN} python


.PHONY: format
format:
	${RUN} isort --virtual-env "${VENV}" "${HERE}/src"
	${RUN} isort --virtual-env "${VENV}" "${HERE}/serverless/src"
	${RUN} black "${HERE}/src"
	${RUN} black "${HERE}/serverless/src"


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


.PHONY: static
static:
	PYTHONPATH="${PYTHONPATH}" ${PY} src/manage.py collectstatic --no-input


.PHONY: sls
sls:
	(cd "${HERE}/serverless" && sls deploy)


.PHONY: wipe
wipe: wipe-static wipe-sls


.PHONY: wipe-static
wipe-static:
	rm -rf "${HERE}/.static/"


.PHONY: wipe-sls
wipe-sls:
	rm -rf "${HERE}/serverless/.serverless/"
