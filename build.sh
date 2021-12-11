#!/bin/bash
docker build --no-cache -t hackinglab/alpine-python-flask-http-request-catcher:3.2.0 -t hackinglab/alpine-python-flask-http-request-catcher:3.2 -t hackinglab/alpine-python-flask-http-request-catcher:latest -f Dockerfile .
