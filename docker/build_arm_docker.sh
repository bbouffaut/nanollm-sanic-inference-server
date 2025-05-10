#!/bin/bash

TAG=$1
PLATFORM=$2

# llama_cpp + nanollm container based only
# docker buildx build --push --platform $PLATFORM -t registry.gitlab.com/skails/jetson-nano/venv-3.10-llama_cpp-nanollm-cuda:$TAG -f ./docker/Dockerfile .

# llama-cpp + mlc_llm
docker buildx build --push --platform $PLATFORM -t registry.gitlab.com/skails/jetson-nano/venv-3.10-llama_cpp-mlc-cuda:$TAG -f ./docker/Dockerfile .