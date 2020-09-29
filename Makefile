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
	rm -rf "${DIR_REPO}/.static/"


.PHONY: wipe-sls
wipe-sls:
	rm -rf "$(DIR_SERVERLESS)/.serverless/"
