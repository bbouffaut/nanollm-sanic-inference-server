
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

    name: str = "MLCModel"
    has_arguments: bool = True

    def __init__(self, model_path: str, gpu: bool, model_lib: str = None):
        device_map = 'cuda' if gpu else 'cpu'
        self.model = model_path
        self.engine = MLCEngine(model_path, mode='local', device=device_map, model_lib=model_lib)
        logger.info(f'MLC Model instance created with params with {model_path}')
          

    async def generate_stream(self, messages):
        logger.debug(f"MLC GenerateSTREAM with model {self.model} and messages {messages}")
        for response in self.engine.chat.completions.create(
            messages=messages,
            model=self.model,
            stream=True,
        ):
            for chunk in response:
                yield chunk 
        
    
    async def generate(self, messages, max_tokens=100, temperature=0.7):
        logger.debug(f"MLC Generate with model {self.model} and messages {messages}")
        response = self.engine.chat.completions.create(
            messages=messages,
            model=self.model,
            stream=False,
        )

        logger.debug(f"Response From LLM = {response.choices[0]}")

        
        return response.choices[0]
    
    def close(self):
        self.engine.terminate()

        