#!/bin/bash

TAG=$1
PLATFORM=$2

docker buildx build --platform $PLATFORM -t venv-3.12-llama_cpp-cuda:$TAG -f ./docker/Dockerfile .
