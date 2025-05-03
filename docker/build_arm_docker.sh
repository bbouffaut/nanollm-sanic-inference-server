#!/bin/bash

TAG=$1
PLATFORM=$2

docker buildx build --platform $PLATFORM -t nanollm-sanic-inference-server:$TAG -f ./docker/Dockerfile .
