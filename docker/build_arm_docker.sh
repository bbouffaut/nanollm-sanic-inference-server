#!/bin/bash

TAG=$1
PLATFORM=$2

docker buildx build --push --platform $PLATFORM -t registry.gitlab.com/skails/jetson-nano/venv-3.12-llama_cpp-cuda:$TAG -f ./docker/Dockerfile .
