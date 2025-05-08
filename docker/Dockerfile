#FROM dustynv/nano_llm:24.5-r36.2.0
FROM llamacpp:r36.4.3-llama_cpp
# BUILD llamacpp:r36.4.3-llama_cpp this image with: 
# jetson-containers build --name=llamacpp llama_cpp

USER root
RUN apt update && apt install -y vim

RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/usr/local/bin" sh

WORKDIR /root
RUN /bin/bash -c "uv venv venv-3.12-llama_cpp-CUDA --python 3.12"
RUN /bin/bash -c "source venv-3.12-llama_cpp-CUDA/bin/activate"

# https://github.com/abetlen/llama-cpp-python/issues/1779#issuecomment-2396550099
RUN CUDACXX=/usr/local/cuda/bin/nvcc CMAKE_ARGS="-DGGML_CUDA=on" FORCE_CMAKE=1 VIRTUAL_ENV=/root/venv-3.12-llama_cpp-CUDA uv pip install llama-cpp-python --no-cache-dir --force-reinstall --upgrade