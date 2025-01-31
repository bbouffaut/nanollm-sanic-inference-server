
from llama_cpp import Llama
from src.constants import MODEL_FILE, MODEL_PATH
from src.model_adapter import ModelAdapter


def llama_cpp_generate(messages, llm, temperature):
    response = llm.create_chat_completion(
        messages=messages,
        temperature=temperature,
        stream=False
    )
    print(f'Response: {response}')
    return response
    

async def llama_cpp_generate_stream(messages, llm, temperature):
    response = llm.create_chat_completion(
        messages=messages,
        temperature=temperature,
        stream=True
    )
    for chunk in response:
        yield chunk
    

def generate_prompt(messages):
    prompt = ""
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        prompt += f"{role}: {content}\n"
    return prompt
# Replace the model with mock functions
class LlamaCppModel(ModelAdapter):

    name: str = "LlamaCppModel"
    model_local_path_for_tokenizer: str|None = MODEL_PATH

    def __init__(self):
        self.llm = Llama(model_path=MODEL_PATH + "/" + MODEL_FILE, chat_format="chatml", n_gpu_layers=-1)

    async def generate(self, messages, max_tokens=100, temperature=0.7):
        return llama_cpp_generate(messages, self.llm, temperature)
    
    async def generate_stream(self, messages, max_tokens=100, temperature=0.7):
        async for chunk in llama_cpp_generate_stream(messages, self.llm, temperature):
            yield chunk