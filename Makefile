llama-server-gemma2:
	export ENV_FILE_PATH=./config/.env && PYTHONPATH=. uv run -m sanic src.apps.llama_cpp_server:app --port=9010 --workers=1

echo-server:
	export ENV_FILE_PATH=./config/.env && PYTHONPATH=. uv run -m sanic src.apps.echo_server:app --dev --port=9010

echo-server-with-tokenizer:
	export ENV_FILE_PATH=./config/.env && PYTHONPATH=. uv run -m sanic src.apps.echo_server_with_tpkenizer:app --dev --port=9010

mock-server:
	export ENV_FILE_PATH=./config/.env && PYTHONPATH=. uv run -m sanic src.apps.mock_server:app --dev --port=9010
