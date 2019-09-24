IMAGE_NAME=cvisionai/thumbnail_extractor:latest-$(shell whoami)

build:
	docker build -t $(IMAGE_NAME) -f tator/Dockerfile .

.PHONY: test
test:
	bash test/test.sh

.PHONY: docker_test
docker_test: config.json
	rm -rf tmp/*
	tator_testHarness.py config.json tator/setup.py
	docker run --rm -v$(shell pwd)/tmp:/work -eTATOR_WORK_DIR=/work $(IMAGE_NAME)
	tator_testHarness.py config.json tator/teardown.py
