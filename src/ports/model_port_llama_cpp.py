
from llama_cpp import Llama
from src.adapters.model_adapter import ModelAdapter
from src.types.model_info_type import ModelParams
from src.utils.logger import logger


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
    has_arguments: bool = True

    def __init__(self, model_params: ModelParams):
        model_path = model_params.path
        #import traceback
        n_gpu_layers = -1 if model_params.gpu else 0
        self.llm = Llama(model_path=model_path, chat_format="chatml", n_gpu_layers=n_gpu_layers)
        logger.info(f"Initialized LlamaCppModel with model path: {model_path} and gpu: {model_params.gpu}")
        # traceback.print_stack()  # Show where it's being called from

    async def generate(self, messages, max_tokens=100, temperature=0.7):
        return llama_cpp_generate(messages, self.llm, temperature)
    
    async def generate_stream(self, messages, max_tokens=100, temperature=0.7):
        async for chunk in llama_cpp_generate_stream(messages, self.llm, temperature):
            yield chunk