# launch sanic server in dev mode
`export ENV_FILE_PATH=./config/.env && sanic llama_cpp_server:app --dev`

# launch sanic server in prod mode (single process)
`export ENV_FILE_PATH=./config/.env && sanic llama_cpp_server:app --single-process`