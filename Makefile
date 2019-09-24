IMAGE_NAME=cvisionai/thumbnail_extractor:latest-$(shell whoami)

build:
	docker build -t $(IMAGE_NAME) -f tator/Dockerfile .

.PHONY: test
test:
	bash test/test.sh
