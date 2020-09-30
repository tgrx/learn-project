include Makefile.variables.mk


.PHONY: setup
setup:
	$(call log, setting up everything)
	$(PYTHON) $(DIR_SCRIPTS)/setup_pycharm.py


.PHONY: format
format:
	$(call log, reorganizing imports & formatting code)
	$(RUN) isort --virtual-env="$(DIR_VENV)" "$(DIR_SRC)" "$(DIR_SERVERLESS_SRC)"
	$(RUN) black "$(DIR_SRC)" "$(DIR_SERVERLESS_SRC)"


.PHONY: run
run:
	$(call log, starting django server)
	$(PYTHON) src/manage.py runserver


.PHONY: migrate
migrate:
	$(call log, applying migrations)
	$(PYTHON) src/manage.py migrate


.PHONY: migrations
migrations:
	$(call log, generating migrations)
	$(PYTHON) src/manage.py makemigrations


.PHONY: su
su:
	$(call log, creating a new superuser)
	$(PYTHON) src/manage.py createsuperuser


.PHONY: sh
sh:
	$(call log, starting django shell)
	$(PYTHON) src/manage.py shell


.PHONY: static
static:
	$(call log, collecting static)
	$(PYTHON) src/manage.py collectstatic --no-input


.PHONY: sls
sls:
	(cd "$(DIR_SERVERLESS)" && sls deploy)


.PHONY: wipe
wipe: wipe-static wipe-sls


.PHONY: wipe-static
wipe-static:
	rm -rf "$(DIR_REPO)/.static/"


.PHONY: wipe-sls
wipe-sls:
	rm -rf "$(DIR_SERVERLESS)/.serverless/"


.PHONY: resetdb
resetdb:  dropdb createdb migrations migrate
	$(call log, resetting db to initial state)


.PHONY: dropdb
dropdb:
	$(call log, dropping database)
	psql -d postgres -c "DROP DATABASE IF EXISTS $(shell $(PYTHON) $(DIR_SCRIPTS)/get_db_name.py);"


.PHONY: createdb
createdb:
	$(call log, creating database)
	psql -d postgres -c "CREATE DATABASE $(shell $(PYTHON) $(DIR_SCRIPTS)/get_db_name.py);"
