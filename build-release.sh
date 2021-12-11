#!/bin/bash
docker build --no-cache -t hackinglab/alpine-python-flask-http-request-catcher:$1.0 -t hackinglab/alpine-python-flask-http-request-catcher:$1 -t hackinglab/alpine-python-flask-http-request-catcher:latest -f Dockerfile .

docker push hackinglab/alpine-python-flask-http-request-catcher
docker push hackinglab/alpine-python-flask-http-request-catcher:$1
docker push hackinglab/alpine-python-flask-http-request-catcher:$1.0

