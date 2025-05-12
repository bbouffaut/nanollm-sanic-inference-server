
from threading import Thread
from src.adapters.model_adapter import ModelAdapter
from src.utils.logger import logger

from mlc_llm import MLCEngine


def transformers_generate(messages, llm, temperature):
    response = llm.create_chat_completion(
        messages=messages,
        temperature=temperature,
        stream=False
    )
    print(f'Response: {response}')
    return response
    

async def transformers_generate_stream(messages, llm, temperature):
    response = llm.create_chat_completion(
        messages=messages,
        temperature=temperature,
        stream=True
    )
    for chunk in response:
        yield chunk
    
# Replace the model with mock functions
class MLCModel(ModelAdapter):

    name: str = "LlamaCppModel"
    has_arguments: bool = True

    def __init__(self, model_path: str, gpu: bool):
        device_map = 'cuda' if gpu else 'cpu'
        self.model = model_path
        self.engine = MLCEngine(model_path, mode='local', device=device_map)
          

    async def generate_stream(self, messages):
        for response in self.engine.chat.completions.create(
            messages=messages,
            model=self.model,
            stream=True,
        ):
            for chunk in response:
                yield chunk 
        
    
    async def generate(self, messages, max_tokens=100):
        response = self.engine.chat.completions.create(
            messages=messages,
            model=self.model,
            stream=False,
        )
        
        return response

        