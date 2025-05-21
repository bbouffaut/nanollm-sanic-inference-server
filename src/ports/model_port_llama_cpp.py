
from typing import Any, AsyncGenerator
from llama_cpp import Llama
from src.adapters.model_adapter import ModelAdapter
from src.adapters.openai.openai_api_protocol import ChatCompletionResponse, ChatCompletionStreamResponse, CompletionResponse
from src.utils.logger import logger

def add_role_to_choices(chunk, role):

    if 'choices' in chunk:
        for choice in chunk['choices']:
            if 'delta' in choice:
                if 'role' not in choice['delta'] or choice['delta']['role'] is None:
                    choice['delta']['role'] = role
    
    return chunk

def llama_cpp_generate_chat(messages, llm, max_tokens, temperature) -> CompletionResponse:
    response: ChatCompletionResponse = llm.create_chat_completion(
        messages=messages,
        temperature=temperature,
        stream=False,
        max_tokens=max_tokens
    )
    logger.debug(f'llama.cpp response: {response}')
    return ChatCompletionResponse(**{**response, 'finish_reason': 'stop'})
    

async def llama_cpp_generate_chat_stream(messages, llm, max_tokens, temperature) -> AsyncGenerator[CompletionResponse, Any]:
    response: ChatCompletionStreamResponse = llm.create_chat_completion(
        messages=messages,
        temperature=temperature,
        stream=True,
        max_tokens=max_tokens
    )
    logger.debug(f"llama.ccp Response: {response}")
    for chunk in response:
        chunk = add_role_to_choices(chunk, 'assistant')
        logger.debug(f"llama.cpp chunk = {chunk}")
        yield ChatCompletionStreamResponse(**{**chunk, 'finish_reason': None})

def llama_cpp_generate(prompt, llm, max_tokens, temperature) -> CompletionResponse:
    response: CompletionResponse = llm.create_completion(
        prompt=prompt,
        temperature=temperature,
        stream=False,
        max_tokens=max_tokens
    )
    logger.debug(f'llama.cpp response: {response}')
    return CompletionResponse(**response)
    

async def llama_cpp_generate_stream(prompt, llm, max_tokens, temperature) -> AsyncGenerator[CompletionResponse, Any]:
    response: CompletionResponse = llm.create_completion(
        prompt=prompt,
        temperature=temperature,
        stream=True,
        max_tokens=max_tokens
    )
    logger.debug(f"llama.ccp Response: {response}")
    for chunk in response:
        logger.debug(f"llama.cpp chunk = {chunk}")
        yield CompletionResponse(**chunk) # CompletionResponse
    

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

    def __init__(self, model_path: str, gpu: bool):
        #import traceback
        n_gpu_layers = -1 if gpu else 0
        self.llm = Llama(model_path=model_path, chat_format="chatml", n_gpu_layers=n_gpu_layers)
        logger.info(f"Initialized LlamaCppModel with model path: {model_path} and gpu: {gpu}")
        # traceback.print_stack()  # Show where it's being called from

    async def generate_chat(self, messages, max_tokens=100, temperature=0.7) -> CompletionResponse:
        return llama_cpp_generate_chat(messages, self.llm, max_tokens, temperature)
    
    async def generate_chat_stream(self, messages, max_tokens=100, temperature=0.7) -> AsyncGenerator[CompletionResponse, Any]:
        async for chunk in llama_cpp_generate_chat_stream(messages, self.llm, max_tokens, temperature):
            yield chunk

    async def generate(self, prompt, max_tokens=100, temperature=0.7) -> CompletionResponse:
        return llama_cpp_generate(prompt, self.llm, max_tokens, temperature)
    
    async def generate_stream(self, prompt, max_tokens=100, temperature=0.7) -> AsyncGenerator[CompletionResponse, Any]:
        async for chunk in llama_cpp_generate_stream(prompt, self.llm, max_tokens, temperature):
            yield chunk

    def get_stats(self):
        logger.info(f"Context = {self.llm.ctx}")