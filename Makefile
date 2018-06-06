VENV := venv
BIN := $(VENV)/bin

export DEFAULT_IMAGES_PATH := $(CURDIR)/i
export DEFAULT_METADATA_PATH := $(CURDIR)/m
export PORTRA_SETTINGS := $(CURDIR)/settings.py
export SECRET_KEY := cat $(CURDIR)/SECRET_KEY

$(VENV): setup.py requirements.txt
	python ./vendor/venv-update venv= venv -p python3 install= -r requirements.txt

.PHONY: clean
clean:
	rm -rf $(VENV) *.egg-info build dist

.PHONY: dev
dev:
	$(BIN)/python run.py

.PHONY: secret
secret:
	openssl rand -base64 32 >> SECRET_KEY

settings.py:
	ln -fs settings/settings.py settings.py

.PHONY: update-requirements
update-requirements:
	$(eval TMP := $(shell mktemp -d))
	python ./vendor/venv-update venv= $(TMP) -p python3 install= .
	. $(TMP)/bin/activate && \
		pip freeze | sort | grep -vE '^(portra|venv-update)==' > requirements.txt
	rm -rf $(TMP)
