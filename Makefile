# /!\ CREATE a .venv folder by:
# 1 - Running uv venv && uv sync into jetson-nano
# 2 - Copying a .venv folder from somewhere else (jetson-nanao container image as an example)

llama-server-gemma2:
	export ENV_FILE_PATH=./config/.env && PYTHONPATH=. MODEL_PARAMS_ID='llama-server-gemma2'  uv run -m src.apps.sanic_app

echo-server:
	export ENV_FILE_PATH=./config/.env && PYTHONPATH=. MODEL_PARAMS_ID='echo-server'  uv run -m src.apps.sanic_app

echo-server-with-tokenizer:
	export ENV_FILE_PATH=./config/.env && PYTHONPATH=. MODEL_PARAMS_ID='echo-server-with-tokenizer'  uv run -m src.apps.sanic_app

mock-server:
	export ENV_FILE_PATH=./config/.env && PYTHONPATH=. MODEL_PARAMS_ID='mock-server' uv run -m src.apps.sanic_app

hello-world:
	PYTHONPATH=. uv run -m src.apps.hello-world

test-cuda:
	uv run tests/test-cuda.py

test-cuda-llama-cpp:
	uv run tests/test-cuda-llama-cpp.py

