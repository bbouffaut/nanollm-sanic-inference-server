# /!\ CREATE a .venv folder by:
# 1 - Running uv venv && uv sync into jetson-nano
# 2 - Copying a .venv folder from somewhere else (jetson-nanao container image as an example)

llama-server-gemma2:
	export ENV_FILE_PATH=./config/.env && PYTHONPATH=. MODEL_PARAMS_ID='llama-server-gemma2'  uv run -m src.apps.sanic_app --port=9010 --workers=1

echo-server:
	export ENV_FILE_PATH=./config/.env && PYTHONPATH=. MODEL_PARAMS_ID='echo-server'  uv run -m src.apps.sanic_app --port=9010

echo-server-with-tokenizer:
	export ENV_FILE_PATH=./config/.env && PYTHONPATH=. MODEL_PARAMS_ID='echo-server-with-tokenizer'  uv run -m src.apps.sanic_app --port=9010

mock-server:
	export ENV_FILE_PATH=./config/.env && PYTHONPATH=. MODEL_PARAMS_ID='mock-server' uv run -m src.apps.sanic_app --dev --port=9010

hello-world:
	PYTHONPATH=. uv run -m src.apps.hello-world

