#!/bin/bash

set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <version>" >&2
    exit 1
fi

version=$1
image=hackinglab/alpine-python-flask-http-request-catcher
platforms=linux/arm64,linux/amd64

docker buildx build --platform "$platforms" -t "$image:latest" . --push
docker buildx build --platform "$platforms" -t "$image:$version" . --push
docker buildx build --platform "$platforms" -t "$image:$version.0" . --push
