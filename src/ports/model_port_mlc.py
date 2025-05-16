
from typing import Any, AsyncGenerator
from src.adapters.model_adapter import ModelAdapter
from src.adapters.openai.openai_api_protocol import ChatCompletionResponse, ChatCompletionStreamResponse, CompletionResponse
from src.utils.logger import logger

from mlc_llm import MLCEngine


class MLCModel(ModelAdapter):

    name: str = "MLCModel"
    has_arguments: bool = True

    def __init__(self, model_path: str, gpu: bool, model_lib: str = None):
        device_map = 'cuda' if gpu else 'cpu'
        self.model = model_path
        self.engine = MLCEngine(model_path, mode='local', device=device_map, model_lib=model_lib)
        logger.info(f'MLC Model instance created with params with {model_path}')
          

    async def generate_stream(self, messages) -> AsyncGenerator[CompletionResponse, Any]:
        logger.debug(f"MLC GenerateSTREAM with model {self.model} and messages {messages}")
        for response in self.engine.chat.completions.create(
            messages=messages,
            model=self.model,
            stream=True,
        ):
            for chunk in response:
                yield ChatCompletionStreamResponse(**chunk) 
        
    
    async def generate(self, messages, max_tokens=100, temperature=0.7) -> ChatCompletionResponse:
        logger.debug(f"MLC Generate with model {self.model} and messages {messages}")
        response: ChatCompletionResponse = self.engine.chat.completions.create(
            messages=messages,
            model=self.model,
            stream=False,
        )

        logger.debug(f"Response From LLM = {response}")

        return ChatCompletionResponse(**response)
    
    def close(self):
        self.engine.terminate()
        