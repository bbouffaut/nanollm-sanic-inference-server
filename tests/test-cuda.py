from llama_cpp import Llama
llm = Llama(model_path='/data/models/huggingface/gemma-2-2b-it-Q3_K_L.gguf', chat_format="chatml", n_gpu_layers=-1)

prompt = """[INST] <<SYS>>
Name the planets in the solar system? 
<</SYS>>
[/INST] 
"""
output = llm(prompt, max_tokens=350, echo=True)
print(output['choices'][0]['text'].split('[/INST]')[-1])
