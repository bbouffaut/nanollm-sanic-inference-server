# update /root/.cache/mlc_llm/mlc-ai/gemma-2-2b-it-q4f16_1-MLC/mlc_llm-chat.config Before compiling

mlc_llm compile --device cuda --opt O3 \
    --output /data/models/mlc_llm/model_lib/gemma-2-2b-it-q4f16_1-mlc_aarch64-cu126-sm87.so \
    --overrides="tensor_parallel_shards=1;context_window_size=8192;prefill_chunk_size=4096" \
    /data/models/mlc_llm/mlc-ai/gemma-2-2b-it-q4f16_1-MLC/mlc-chat-config.json

#mlc_llm compile --device cuda --opt O3 \
#    --output /data/models/mlc_llm/model_lib/llama-3.1-8b-instruct-q4f16_ft-mlc-aarch64-cu126-sm87.so \
#    --overrides="tensor_parallel_shards=1;context_window_size=8192;prefill_chunk_size=4096" \
#    /data/models/mlc_llm/dusty-nv/Llama-3.1-8B-Instruct-q4f16_ft-MLC/mlc-chat-config.json
