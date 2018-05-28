VENV := venv
BIN := $(VENV)/bin

$(VENV): setup.py requirements.txt
	python ./vendor/venv-update venv= venv -p python3 install= -r requirements.txt

.PHONY: clean
clean:
	rm -rf $(VENV) *.egg-info build dist

.PHONY: dev
dev:
	$(BIN)/python run.py

.PHONY: update-requirements
update-requirements:
	$(eval TMP := $(shell mktemp -d))
	python ./vendor/venv-update venv= $(TMP) -p python3 install= .
	. $(TMP)/bin/activate && \
		pip freeze | sort | grep -vE '^(portra|venv-update)==' > requirements.txt
	rm -rf $(TMP)
