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
#https://medium.com/@ryan.stewart113/a-simple-guide-to-enabling-cuda-gpu-support-for-llama-cpp-python-on-your-os-or-in-containers-8b5ec1f912a4
# RUN CUDACXX=/usr/local/cuda/bin/nvcc CMAKE_ARGS="-DGGML_CUDA=on -DCMAKE_CUDA_ARCHITECTURES=native" FORCE_CMAKE=1 VIRTUAL_ENV=/root/venv-3.12-llama_cpp-CUDA uv pip install llama-cpp-python --no-cache-dir --force-reinstall --upgrade

RUN wget https://pypi.jetson-ai-lab.dev/jp6/cu126/+f/213/c44ff20e1dd8a/llama_cpp_python-0.3.8-cp310-cp310-linux_aarch64.whl#sha256=213c44ff20e1dd8ad3ed84f9a0a6e8f2a032df4dabaeb8ae19a611d9e59cfe5b
RUN VIRTUAL_ENV=/root/venv-3.12-llama_cpp-CUDA uv run pip install llama_cpp_python-0.3.8-cp310-cp310-linux_aarch64.whl