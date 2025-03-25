llama-server-gemma2:
	export ENV_FILE_PATH=./config/.env && sanic src.apps.llama_cpp_server:app --dev --model=gemma-2-2b-it-GGUF/gemma-2-2b-it-Q4_K_M.gguf

echo-server:
	export ENV_FILE_PATH=./config/.env && sanic src.apps.echo_server:app --dev

echo-server-with-tokenizer:
	export ENV_FILE_PATH=./config/.env && sanic src.apps.echo_server_with_tpkenizer:app --dev

mock-server:
	export ENV_FILE_PATH=./config/.env && sanic src.apps.mock_server:app --dev
