llama-server-gemma2:
	export ENV_FILE_PATH=./config/.env && PYTHONPATH=. uv run -m sanic src.apps.llama_cpp_server:app --model_path=gemma-2-2b-it-GGUF/gemma-2-2b-it-Q4_K_M.gguf --port=10000

echo-server:
	export ENV_FILE_PATH=./config/.env && PYTHONPATH=. uv run -m sanic src.apps.echo_server:app --dev --port=10000

echo-server-with-tokenizer:
	export ENV_FILE_PATH=./config/.env && PYTHONPATH=. uv run -m sanic src.apps.echo_server_with_tpkenizer:app --dev --port=10000

mock-server:
	export ENV_FILE_PATH=./config/.env && PYTHONPATH=. uv run -m sanic src.apps.mock_server:app --dev --port=10000
