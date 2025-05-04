#FROM dustynv/nano_llm:24.5-r36.2.0
FROM llamacpp:r36.4.3-llama_cpp
# BUILD this image with: 
# jetson-containers build --name=llamacpp llama_cpp

USER root
RUN apt update && apt install -y vim

RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/usr/local/bin" sh

COPY . /nanollm-sanic-inference-server
WORKDIR /nanollm-sanic-inference-server

RUN /bin/bash -c "source .venv/bin/activate"
RUN CUDACXX=/usr/local/cuda/bin/nvcc CMAKE_ARGS="-DGGML_CUDA=on -DCMAKE_CUDA_ARCHITECTURES=all-major" uv run pip install llama-cpp-python --no-cache-dir --force-reinstall --upgrade

EXPOSE 9010
