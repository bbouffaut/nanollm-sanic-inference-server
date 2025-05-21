
from typing import Any, AsyncGenerator, Optional
from src.adapters.model_adapter import ModelAdapter
from src.adapters.openai.openai_api_protocol import ChatCompletionResponse, ChatCompletionStreamResponse, CompletionResponse
from src.utils.logger import logger

from mlc_llm import AsyncMLCEngine



class MLCModel(ModelAdapter):

    name: str = "MLCModel"
    has_arguments: bool = True

    def __init__(self, model_path: str, gpu: bool, model_lib: str = None):
        device_map = 'cuda' if gpu else 'cpu'
        self.model = model_path
        self.engine = AsyncMLCEngine(model_path, mode='local', device=device_map, model_lib=model_lib)
        logger.info(f'MLC Model instance created with params with {model_path}')
          

    async def generate_chat_stream(self, messages, max_tokens: Optional[int], temperature: Optional[float]) -> AsyncGenerator[CompletionResponse, Any]:
        logger.debug(f"MLC ChatGenerateSTREAM with model {self.model} and messages {messages}")
        async for chunk in await self.engine.chat.completions.create(
            messages=messages,
            model=self.model,
            stream=True,
            stream_options = {
                "include_usage": True
            }
        ):
            logger.debug(f"MLC chunk = {chunk}")
            yield chunk #ChatCompletionStreamResponse type
        
    
    async def generate_chat(self, messages, max_tokens=100, temperature=0.7) -> ChatCompletionResponse:
        logger.debug(f"MLC ChatGenerate with model {self.model} and messages {messages}")
        response: ChatCompletionResponse = await self.engine.chat.completions.create(
            messages=messages,
            model=self.model,
            stream=False,
        )

        logger.debug(f"Response From LLM = {response}")

        return response
    
    async def generate_stream(self, prompt, max_tokens: Optional[int], temperature: Optional[float]) -> AsyncGenerator[CompletionResponse, Any]:
        logger.debug(f"MLC GenerateSTREAM with model {self.model} and prompt {prompt}")
        async for chunk in await self.engine.completions.create(
            prompt=prompt,
            model=self.model,
            stream=True,
            stream_options = {
                "include_usage": True
            }
        ):
            logger.debug(f"MLC chunk = {chunk}")
            yield chunk #CompletionStreamResponse type
        
    
    async def generate(self, prompt, max_tokens=100, temperature=0.7) -> CompletionResponse:
        logger.debug(f"MLC Generate with model {self.model} and prompt {prompt}")
        response: CompletionResponse = await self.engine.completions.create(
            prompt=prompt,
            model=self.model,
            stream=False
        )

        logger.debug(f"Response From LLM = {response}")

        return response
    
    def close(self):
        self.engine.terminate()
        
    def get_stats(self):
        pass