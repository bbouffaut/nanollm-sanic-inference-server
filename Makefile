llama-server-gemma2:
	export ENV_FILE_PATH=./config/.env && PYTHONPATH=. MODEL_PARAMS_ID='llama-server-gemma2' uv run -m sanic src.apps.sanic_app:app --port=9010 --workers=1

echo-server:
	export ENV_FILE_PATH=./config/.env && PYTHONPATH=. MODEL_PARAMS_ID='echo-server' uv run -m sanic src.apps.sanic_app:app --dev --port=9010

echo-server-with-tokenizer:
	export ENV_FILE_PATH=./config/.env && PYTHONPATH=. MODEL_PARAMS_ID='echo-server-with-tokenizer' uv run -m sanic src.apps.sanic_app:app --dev --port=9010

mock-server:
	export ENV_FILE_PATH=./config/.env && PYTHONPATH=. MODEL_PARAMS_ID='mock-server' uv run -m sanic src.apps.sanic_app:app --dev --port=9010
