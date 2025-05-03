from llama_cpp import Llama
llm = Llama(model_path='/models/huggingface/gemma-2-2b-it-Q3_K_L.gguf', chat_format="chatml", n_gpu_layers=-1)
