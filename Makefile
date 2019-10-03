PRODUCT_NAME=cvisionai/frame_extractor
IMAGE_NAME=$(PRODUCT_NAME):latest-$(shell whoami)
PUBLISHED_NAME=${DOCKERHUB_USER}/$(PRODUCT_NAME):latest

ARGUMENTS=$(shell cat config.json | jq .TATOR_PIPELINE_ARGS)

build:
	docker build -t $(IMAGE_NAME) -f tator/Dockerfile .

.PHONY: test
test:
	bash test/test.sh

.PHONY: docker_test
docker_test: config.json
	mkdir -p tmp
	docker run --rm -v$(shell pwd)/tmp:/work -eTATOR_WORK_DIR=/work $(IMAGE_NAME) clean.sh 
	tator_testHarness.py config.json tator/setup.py
	docker run --rm -v$(shell pwd)/tmp:/work -eTATOR_WORK_DIR=/work -eTATOR_PIPELINE_ARGS=$(ARGUMENTS) $(IMAGE_NAME)
	tator_testHarness.py config.json tator/teardown.py

.PHONY: publish
publish:
	docker tag $(IMAGE_NAME) $(PUBLISHED_NAME)
	docker push $(PUBLISHED_NAME)
