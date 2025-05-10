#FROM dustynv/nano_llm:24.5-r36.2.0
# FROM llamacpp:r36.4.3-llama_cpp
# BUILD llamacpp:r36.4.3-llama_cpp this image with: 
# jetson-containers build --name=llamacpp triton llama_cpp

# https://hub.docker.com/u/dustynv
FROM  dustynv/llama_cpp:r36.4.0

USER root
# https://forums.developer.nvidia.com/t/libopenblas-so-0-not-found/264406
RUN apt update && apt install -y vim && apt install -y libopenblas-dev

# https://github.com/abetlen/llama-cpp-python/issues/1779#issuecomment-2396550099
#https://medium.com/@ryan.stewart113/a-simple-guide-to-enabling-cuda-gpu-support-for-llama-cpp-python-on-your-os-or-in-containers-8b5ec1f912a4
# RUN CUDACXX=/usr/local/cuda/bin/nvcc CMAKE_ARGS="-DGGML_CUDA=on -DCMAKE_CUDA_ARCHITECTURES=native" FORCE_CMAKE=1 VIRTUAL_ENV=/root/venv-3.10-llama_cpp-CUDA uv pip install llama-cpp-python --no-cache-dir --force-reinstall --upgrade

RUN pip install torch
RUN pip install torchvision
RUN pip install torchaudio
RUN pip install mlc_llm
RUN pip install tvm

RUN pip uninstall --yes transformers
RUN pip install transformers

COPY . /nanollm-sanic-inference-server
WORKDIR /nanollm-sanic-inference-server

RUN pip install -r requirements.txt

