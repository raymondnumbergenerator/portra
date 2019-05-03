VENV := venv
BIN := $(VENV)/bin

export DEFAULT_IMAGES_PATH := $(CURDIR)/i
export DEFAULT_METADATA_PATH := $(CURDIR)/m
export PORTRA_SETTINGS := $(CURDIR)/settings/settings.py
export SECRET_KEY := $(shell cat $(CURDIR)/SECRET_KEY 2> /dev/null)

$(VENV): setup.py requirements.txt
	python3 ./vendor/venv-update venv= venv -p python3 install= -r requirements.txt

.PHONY: clean
clean:
	rm -rf $(VENV) *.egg-info build dist

.PHONY: dev
dev:
	mkdir -p $(DEFAULT_IMAGES_PATH) $(DEFAULT_METADATA_PATH)
	$(BIN)/python3 run.py

.PHONY: secret
secret:
	openssl rand -base64 32 >> SECRET_KEY

.PHONY: update-requirements
update-requirements:
	$(eval TMP := $(shell mktemp -d))
	python ./vendor/venv-update venv= $(TMP) -p python3 install= .
	. $(TMP)/bin/activate && \
		pip freeze | sort | grep -vE '^(portra|venv-update)==' > requirements.txt
	rm -rf $(TMP)

.PHONY: docker-image
docker-image:
	docker build -t raymondnumbergenerator/portra .

.PHONY: docker-run
docker-run:
	mkdir -p ~/portra_files/i ~/portra_files/m
	docker run --name portra \
		--publish 80:8000 \
		--volume ~/portra_files:/srv/portra/files \
		--user $(shell id -u):$(shell id -g) \
		--restart always \
		--detach \
		raymondnumbergenerator/portra:current

.PHONY: docker-redeploy
docker-redeploy:
	make docker-image
	docker stop portra || true
	docker rm portra || true
	docker rmi raymondnumbergenerator/portra:current || true
	docker tag raymondnumbergenerator/portra:latest raymondnumbergenerator/portra:current
	make docker-run
	docker rmi raymondnumbergenerator/portra:latest || true
