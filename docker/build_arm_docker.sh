#!/bin/bash

TAG=$1
PLATFORM=$2

docker buildx build --platform $PLATFORM -t nanollm-sanic-inference-server-local-dev:$TAG -f ./docker/Dockerfile .
