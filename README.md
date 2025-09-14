# Launch Dev Docker env to LAUNCH MANUALLY sanic server
`/ssd/workspace/nanollm_sanic_inference_server/run-bash.sh`
In Docker container:
`cd /workspace/nanollm_sanic_inference_server/`
`make llama-server-gemma3`

# Launch Prod Docker env to LAUNCH SERVER directly
### (DOES NOT WORK SINCE DOCKER IMAGE IS NOT UPDATED)
`/ssd/workspace/nanollm_sanic_inference_server/run-mlc-server.sh llama-server-hermes-llama-3-8b`


# launch sanic server in dev mode
`export ENV_FILE_PATH=./config/.env && sanic llama_cpp_server:app --dev`

# launch sanic server in prod mode (single process)
`export ENV_FILE_PATH=./config/.env && sanic llama_cpp_server:app --single-process`