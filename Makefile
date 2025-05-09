# /!\ CREATE a .venv folder by:
# 1 - Running uv venv && uv sync into jetson-nano
# 2 - Copying a .venv folder from somewhere else (jetson-nanao container image as an example)

llama-server-gemma2:
	ENV_FILE_PATH=./config/.env PYTHONPATH=. MODEL_PARAMS_ID='llama-server-gemma2' python3 -m src.apps.sanic_app

llama-server-gemma3:
	ENV_FILE_PATH=./config/.env PYTHONPATH=. MODEL_PARAMS_ID='llama-server-gemma3' python3 -m src.apps.sanic_app

nanollm-server-gemma2:
	ENV_FILE_PATH=./config/.env PYTHONPATH=. MODEL_PARAMS_ID='nanollm-server-gemma2' python3 -m src.apps.sanic_app

echo-server:
	ENV_FILE_PATH=./config/.env PYTHONPATH=. MODEL_PARAMS_ID='echo-server' python3 -m src.apps.sanic_app

echo-server-with-tokenizer:
	ENV_FILE_PATH=./config/.env PYTHONPATH=. MODEL_PARAMS_ID='echo-server-with-tokenizer' python3 -m src.apps.sanic_app

mock-server:
	ENV_FILE_PATH=./config/.env PYTHONPATH=. MODEL_PARAMS_ID='mock-server' python3 -m src.apps.sanic_app

hello-world:
	PYTHONPATH=. python3 -m src.apps.hello-world

test-cuda:
	python3 tests/test-cuda.py

test-cuda-llama-cpp:
	python3 tests/test-cuda-llama-cpp.py

