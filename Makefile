VENV := venv
BIN := $(VENV)/bin

$(VENV): setup.py requirements.txt
		python ./vendor/venv-update venv= venv -p python3 install= -r requirements.txt

.PHONY: clean
clean:
	rm -rf $(VENV) *.egg-info build dist

.PHONY: dev
dev:
	$(BIN)/python -m portra.run
