#!/bin/bash

set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <version>" >&2
    exit 1
fi

version="$1"

docker buildx build --platform linux/arm64,linux/amd64 -t hackinglab/alpine-python-flask-http-request-catcher:latest . --push
docker buildx build --platform linux/arm64,linux/amd64 -t "hackinglab/alpine-python-flask-http-request-catcher:${version}" . --push
docker buildx build --platform linux/arm64,linux/amd64 -t "hackinglab/alpine-python-flask-http-request-catcher:${version}.0" . --push
