IMAGE_NAME=cvisionai/thumbnail_extractor:latest-$(shell whoami)

build:
	docker build -t $(IMAGE_NAME) -f tator/Dockerfile .

.PHONY: test
test:
	bash test/test.sh

.PHONY: docker_test
docker_test: config.json
	tator_testHarness.py config.json tator/setup.py
	tator_testHarness.py config.json extractor/docker_entry.py
