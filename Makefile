# launch sanic server in dev mode
launch_sanic_server_in_dev_mode:
	export ENV_FILE_PATH=./config/.env && sanic llama_cpp_server:app --dev

# launch sanic server in prod mode (single process)
launch_sanic_server_in_prod_mode:
	export ENV_FILE_PATH=./config/.env && sanic llama_cpp_server:app --single-process