#FROM dustynv/nano_llm:24.5-r36.2.0
# FROM llamacpp:r36.4.3-llama_cpp
# BUILD llamacpp:r36.4.3-llama_cpp this image with: 
# jetson-containers build --name=llamacpp triton llama_cpp
FROM  dustynv/nano_llm:r36.4.0

USER root
# https://forums.developer.nvidia.com/t/libopenblas-so-0-not-found/264406
RUN apt update && apt install -y vim && apt install -y libopenblas-dev

# https://github.com/abetlen/llama-cpp-python/issues/1779#issuecomment-2396550099
#https://medium.com/@ryan.stewart113/a-simple-guide-to-enabling-cuda-gpu-support-for-llama-cpp-python-on-your-os-or-in-containers-8b5ec1f912a4
# RUN CUDACXX=/usr/local/cuda/bin/nvcc CMAKE_ARGS="-DGGML_CUDA=on -DCMAKE_CUDA_ARCHITECTURES=native" FORCE_CMAKE=1 VIRTUAL_ENV=/root/venv-3.10-llama_cpp-CUDA uv pip install llama-cpp-python --no-cache-dir --force-reinstall --upgrade

RUN wget https://pypi.jetson-ai-lab.dev/jp6/cu126/+f/213/c44ff20e1dd8a/llama_cpp_python-0.3.8-cp310-cp310-linux_aarch64.whl#sha256=213c44ff20e1dd8ad3ed84f9a0a6e8f2a032df4dabaeb8ae19a611d9e59cfe5b
RUN pip install llama_cpp_python-0.3.8-cp310-cp310-linux_aarch64.whl

RUN wget https://pypi.jetson-ai-lab.dev/jp6/cu126/+f/6ef/f643c0a7acda9/torch-2.7.0-cp310-cp310-linux_aarch64.whl#sha256=6eff643c0a7acda92734cc798338f733ff35c7df1a4434576f5ff7c66fc97319
RUN pip install torch-2.7.0-cp310-cp310-linux_aarch64.whl

RUN wget https://pypi.jetson-ai-lab.dev/jp6/cu126/+f/daa/bff3a07259968/torchvision-0.22.0-cp310-cp310-linux_aarch64.whl#sha256=daabff3a0725996886b92e4b5dd143f5750ef4b181b5c7d01371a9185e8f0402
RUN pip install torchvision-0.22.0-cp310-cp310-linux_aarch64.whl

RUN wget https://pypi.jetson-ai-lab.dev/jp6/cu126/+f/c59/026d500c57366/torchaudio-2.7.0-cp310-cp310-linux_aarch64.whl#sha256=c59026d500c573666ae0437c4202ac312ac8ebe38fa12dbb37250a07c1e826f9
RUN pip install torchaudio-2.7.0-cp310-cp310-linux_aarch64.whl

RUN wget https://pypi.jetson-ai-lab.dev/jp6/cu126/+f/093/244be85cc5240/mlc_llm-0.20.0-cp310-cp310-linux_aarch64.whl#sha256=093244be85cc5240fdbeeef449b4036a4f641873f5e1018fe80f1b6f944ead86
RUN pip install mlc_llm-0.20.0-cp310-cp310-linux_aarch64.whl

RUN pip uninstall --yes transformers
RUN pip install transformers

COPY . /nanollm-sanic-inference-server
WORKDIR /nanollm-sanic-inference-server

RUN pip install -r requirements.txt

