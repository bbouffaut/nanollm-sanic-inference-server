# /!\ CREATE a .venv folder by:
# 1 - Running uv venv && uv sync into jetson-nano
# 2 - Copying a .venv folder from somewhere else (jetson-nanao container image as an example)

llama-server-gemma2:
	ENV_FILE_PATH=./config/.env MODEL_PARAMS_ID='llama-server-gemma2' python3 -m src.apps.sanic_app

llama-server-gemma3:
	ENV_FILE_PATH=./config/.env MODEL_PARAMS_ID='llama-server-gemma3' python3 -m src.apps.sanic_app

mlc-server-gemma2:
	ENV_FILE_PATH=./config/.env TRANSFORMERS_CACHE=/data/models/huggingface/hub/ HF_HOME=/data/models/huggingface/hub/ MODEL_PARAMS_ID='mlc-server-gemma2' python3 -m src.apps.sanic_app

mlc-server-llama3.2:
	ENV_FILE_PATH=./config/.env TRANSFORMERS_CACHE=/data/models/huggingface/hub/ HF_HOME=/data/models/huggingface/hub/ MODEL_PARAMS_ID='mlc-server-llama3.2' python3 -m src.apps.sanic_app

llama-server-llama3.2:
	ENV_FILE_PATH=./config/.env TRANSFORMERS_CACHE=/data/models/huggingface/hub/ HF_HOME=/data/models/huggingface/hub/ MODEL_PARAMS_ID='llama-server-llama3.2' python3 -m src.apps.sanic_app

echo-server:
	ENV_FILE_PATH=./config/.env MODEL_PARAMS_ID='echo-server' python3 -m src.apps.sanic_app

echo-server-with-tokenizer:
	ENV_FILE_PATH=./config/.env MODEL_PARAMS_ID='echo-server-with-tokenizer' python3 -m src.apps.sanic_app

mock-server:
	ENV_FILE_PATH=./config/.env MODEL_PARAMS_ID='mock-server' python3 -m src.apps.sanic_app

hello-world:
	python3 -m src.apps.hello-world

test-cuda:
	python3 tests/test-cuda.py

test-cuda-llama-cpp:
	python3 tests/test-cuda-llama-cpp.py

test-mlc:
	TRANSFORMERS_CACHE=/data/models/huggingface/hub/ HF_HOME=/data/models/huggingface/hub/ python3 tests/test-mlc.py

# /!\ MUST BE RUN BEFORE MLC server to properly load and compile the binary
# ALSO: rename the *.so file with the name configured in model_param.json file
load-mlc-model-gemma2:
	mlc_llm chat HF://mlc-ai/gemma-2-2b-it-q4f16_1-MLC
