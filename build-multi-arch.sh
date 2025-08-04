#!/bin/bash

docker buildx build --platform linux/arm64,linux/amd64 -t hackinglab/alpine-python-flask-http-request-catcher:latest . --push
docker buildx build --platform linux/arm64,linux/amd64 -t hackinglab/alpine-python-flask-http-request-catcher:$1  . --push
docker buildx build --platform linux/arm64,linux/amd64 -t hackinglab/alpine-python-flask-http-request-catcher:$1.0 . --push

