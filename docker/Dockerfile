#FROM dustynv/nano_llm:24.5-r36.2.0
FROM llamacpp:r36.4.3-llama_cpp

USER root
RUN apt update && apt install -y vim

RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/usr/local/bin" sh

EXPOSE 10000
