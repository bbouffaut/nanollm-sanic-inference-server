import sys
from typing import Any, AsyncGenerator
from llama_cpp import Llama
from src.adapters.model_adapter import ModelAdapter
from src.adapters.openai.openai_api_protocol import ChatCompletionResponse, ChatCompletionStreamResponse, CompletionResponse, CompletionUsage
from src.utils import tracer
from src.utils.constants import N_CTX
from src.utils.logger import logger
import llama_cpp

def add_role_to_choices(chunk, role):

    if 'choices' in chunk:
        for choice in chunk['choices']:
            if 'delta' in choice:
                if 'role' not in choice['delta'] or choice['delta']['role'] is None:
                    choice['delta']['role'] = role
    
    return chunk

def llama_cpp_generate_chat(messages, llm, max_tokens, temperature) -> CompletionResponse:
    response: ChatCompletionResponse = llm.create_chat_completion_openai_v1(
        messages=messages,
        temperature=temperature,
        stream=False,
        max_tokens=max_tokens
    )
    logger.debug(f'llama.cpp response: {response}')
    return ChatCompletionResponse(**{**response.model_dump(), 'finish_reason': 'stop'})
    

async def llama_cpp_generate_chat_stream(messages, llm, max_tokens, temperature) -> AsyncGenerator[CompletionResponse, Any]:
    response: ChatCompletionStreamResponse = llm.create_chat_completion_openai_v1(
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
    response: CompletionResponse = llm.create_completion_openai_v1(
        prompt=prompt,
        temperature=temperature,
        stream=False,
        max_tokens=max_tokens
    )
    logger.debug(f'llama.cpp response: {response}')
    return CompletionResponse(**response)
    

async def llama_cpp_generate_stream(prompt, llm, max_tokens, temperature) -> AsyncGenerator[CompletionResponse, Any]:
    response: CompletionResponse = llm.create_completion_openai_v1(
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
        self.model = model_path
        n_gpu_layers = -1 if gpu else 0
        self.llm = Llama(
            model_path=model_path, 
            chat_format="chatml", 
            n_gpu_layers=n_gpu_layers,
            verbose=True,  # Enable verbose output which includes timing information
            n_ctx=N_CTX
        )
        logger.info(f"Initialized LlamaCppModel with model path: {model_path} and gpu: {gpu}")
        # traceback.print_stack()  # Show where it's being called from

    @tracer.chain
    async def generate_chat(self, messages, max_tokens=100000, temperature=0.7) -> CompletionResponse:
        logger.debug(f"LlamaCpp ChatGenerate with model {self.model} and messages {messages}")
        response = llama_cpp_generate_chat(messages, self.llm, max_tokens, temperature)
        # Get stats and create usage
        stats = self.get_stats()

        response.usage.extra = stats
        return response
    
    @tracer.chain
    async def generate_chat_stream(self, messages, max_tokens=100000, temperature=0.7) -> AsyncGenerator[CompletionResponse, Any]:
        logger.debug(f"LlamaCpp ChatGenerateStream with model {self.model} and messages {messages}")
        async for chunk in llama_cpp_generate_chat_stream(messages, self.llm, max_tokens, temperature):
            # Check if this is the last chunk
            if any(choice.finish_reason == 'stop' for choice in chunk.choices):
                # Get stats and create usage
                stats = self.get_stats()
                # Extract token-related fields and keep the rest in extra
                token_stats = {
                    'prompt_tokens': stats.pop('prompt_tokens', 0),
                    'completion_tokens': stats.pop('eval_tokens', 0),
                    'total_tokens': stats.pop('total_tokens', 0)
                }
                chunk.usage = CompletionUsage(
                    prompt_tokens=token_stats['prompt_tokens'],
                    completion_tokens=token_stats['completion_tokens'],
                    total_tokens=token_stats['total_tokens'],
                    extra=stats
                )
            yield chunk

    @tracer.chain
    async def generate(self, prompt, max_tokens=100000, temperature=0.7) -> CompletionResponse:
        logger.debug(f"LlamaCpp Generate with model {self.model} and prompt {prompt}")
        response = llama_cpp_generate(prompt, self.llm, max_tokens, temperature)
        # Get stats and create usage
        stats = self.get_stats()
        response.usage.extra = stats
        return response
    
    @tracer.chain
    async def generate_stream(self, prompt, max_tokens=100000, temperature=0.7) -> AsyncGenerator[CompletionResponse, Any]:
        logger.debug(f"LlamaCpp GenerateStream with model {self.model} and prompt {prompt}")
        async for chunk in llama_cpp_generate_stream(prompt, self.llm, max_tokens, temperature):
            # Check if this is the last chunk
            if any(choice.finish_reason == 'stop' for choice in chunk.choices):
                # Get stats and create usage
                stats = self.get_stats()
                # Extract token-related fields and keep the rest in extra
                token_stats = {
                    'prompt_tokens': stats.pop('prompt_tokens', 0),
                    'completion_tokens': stats.pop('eval_tokens', 0),
                    'total_tokens': stats.pop('total_tokens', 0)
                }
                chunk.usage = CompletionUsage(
                    prompt_tokens=token_stats['prompt_tokens'],
                    completion_tokens=token_stats['completion_tokens'],
                    total_tokens=token_stats['total_tokens'],
                    extra=stats
                )
            yield chunk

    def get_stats(self):
        #logger.info(f"Context = {self.llm._ctx}") => llama_cpp._internals.LlamaContext
        #self.llm._ctx.print_timings()
        #print(self.llm._model) #=> llama_cpp._internals.LlamaModel 
        stats = self.get_timing_stats()
        logger.debug(f"get_stats(self)  = {stats}")

        return stats

    def get_timing_stats(self):
        """Extract timing statistics from llama.cpp context.
        
        Returns:
            dict: Dictionary containing timing statistics including:
                - load_time_ms: Model load time in milliseconds (t_load_ms)
                - prompt_eval_time_ms: Prompt evaluation time in milliseconds (t_p_eval_ms)
                - prompt_tokens: Number of prompt tokens processed (n_p_eval)
                - prompt_tokens_per_second: Prompt processing speed
                - eval_time_ms: Token generation time in milliseconds (t_eval_ms)
                - eval_tokens: Number of tokens generated (n_eval)
                - eval_tokens_per_second: Token generation speed
                - total_time_ms: Total processing time in milliseconds
                - total_tokens: Total tokens processed
        """
        try:
            if not hasattr(self.llm, '_ctx') or self.llm._ctx is None:
                logger.error("llama.cpp context not available")
                return {}

            # Get performance context data
            perf_data = llama_cpp.llama_perf_context(self.llm._ctx.ctx)
            
            # Initialize stats dictionary with direct field access
            stats = {
                'load_time_ms': perf_data.t_load_ms,
                'prompt_eval_time_ms': perf_data.t_p_eval_ms,
                'prompt_tokens': perf_data.n_p_eval,
                'eval_time_ms': perf_data.t_eval_ms,
                'eval_tokens': perf_data.n_eval
            }
            
            # Calculate derived statistics
            if stats['prompt_eval_time_ms'] > 0:
                stats['prompt_tokens_per_second'] = 1e3 / stats['prompt_eval_time_ms'] * stats['prompt_tokens']
            else:
                stats['prompt_tokens_per_second'] = 0.0
                
            if stats['eval_time_ms'] > 0:
                stats['eval_tokens_per_second'] = 1e3 / stats['eval_time_ms'] * stats['eval_tokens']
            else:
                stats['eval_tokens_per_second'] = 0.0
            
            # Calculate totals
            stats['total_time_ms'] = stats['prompt_eval_time_ms'] + stats['eval_time_ms']
            stats['total_tokens'] = stats['prompt_tokens'] + stats['eval_tokens']
            
            return stats
            
        except Exception as e:
            logger.error(f"Error accessing timing statistics: {e}")
            return {}