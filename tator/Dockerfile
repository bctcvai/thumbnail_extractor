FROM ubuntu:18.04

# Disable interaction
ENV DEBIAN_FRONTEND noninteractive

# Install algorithm dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
build-essential cmake ffmpeg git wget ssh vim \
                python3-pip python3-dev python3-opencv  \
                && apt-get clean && rm -fr /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir wheel setuptools pillow==6.0.0 \
                                progressbar2==3.42.0 pandas==0.24.2

WORKDIR /
COPY extractor /extractor
CMD  [ "python3", "/extractor/docker_entry.py" ]