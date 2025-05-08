# /!\ CREATE a .venv folder by:
# 1 - Running uv venv && uv sync into jetson-nano
# 2 - Copying a .venv folder from somewhere else (jetson-nanao container image as an example)

llama-server-gemma2:
	VIRTUAL_ENV=/root/venv-3.10-llama_cpp-CUDA ENV_FILE_PATH=./config/.env PYTHONPATH=. MODEL_PARAMS_ID='llama-server-gemma2' python3 -m src.apps.sanic_app

echo-server:
	VIRTUAL_ENV=/root/venv-3.10-llama_cpp-CUDA ENV_FILE_PATH=./config/.env PYTHONPATH=. MODEL_PARAMS_ID='echo-server' python3 -m src.apps.sanic_app

echo-server-with-tokenizer:
	VIRTUAL_ENV=/root/venv-3.10-llama_cpp-CUDA ENV_FILE_PATH=./config/.env PYTHONPATH=. MODEL_PARAMS_ID='echo-server-with-tokenizer' python3 -m src.apps.sanic_app

mock-server:
	VIRTUAL_ENV=/root/venv-3.10-llama_cpp-CUDA ENV_FILE_PATH=./config/.env PYTHONPATH=. MODEL_PARAMS_ID='mock-server' python3 -m src.apps.sanic_app

hello-world:
	VIRTUAL_ENV=/root/venv-3.10-llama_cpp-CUDA PYTHONPATH=. python3 -m src.apps.hello-world

test-cuda:
	VIRTUAL_ENV=/root/venv-3.10-llama_cpp-CUDA python3 tests/test-cuda.py

test-cuda-llama-cpp:
	VIRTUAL_ENV=/root/venv-3.10-llama_cpp-CUDA python3 tests/test-cuda-llama-cpp.py

