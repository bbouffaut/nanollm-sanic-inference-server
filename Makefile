llama-server-gemma2:
	export ENV_FILE_PATH=./config/.env && PYTHONPATH=. uv run -m sanic "src.apps.sanic_app:create_app('llama-server-gemma2')" --port=9010 --workers=1

echo-server:
	export ENV_FILE_PATH=./config/.env && PYTHONPATH=. uv run -m sanic "src.apps.sanic_app:create_app('echo-server')" --dev --port=9010

echo-server-with-tokenizer:
	export ENV_FILE_PATH=./config/.env && PYTHONPATH=. uv run -m sanic "src.apps.sanic_app:create_app('echo-server-with-tokenizer')" --dev --port=9010

mock-server:
	export ENV_FILE_PATH=./config/.env && PYTHONPATH=. uv run -m sanic "src.apps.sanic_app:create_app('mock-server')" --dev --port=9010
