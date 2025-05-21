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
        self.llm = Llama(
            model_path=model_path, 
            chat_format="chatml", 
            n_gpu_layers=n_gpu_layers,
            verbose=True  # Enable verbose output which includes timing information
        )
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
        #logger.info(f"Context = {self.llm._ctx}") => llama_cpp._internals.LlamaContext
        #self.llm._ctx.print_timings()
        #print(self.llm._model) #=> llama_cpp._internals.LlamaModel 
        return self.get_timing_stats()

    def get_timing_stats(self):
        """Extract timing statistics from llama.cpp context by capturing print_timings() output.
        
        Returns:
            dict: Dictionary containing timing statistics including:
                - load_time_ms: Model load time in milliseconds
                - prompt_eval_time_ms: Prompt evaluation time in milliseconds
                - prompt_tokens: Number of prompt tokens processed
                - prompt_tokens_per_second: Prompt processing speed
                - eval_time_ms: Token generation time in milliseconds
                - eval_tokens: Number of tokens generated
                - eval_tokens_per_second: Token generation speed
                - total_time_ms: Total processing time in milliseconds
                - total_tokens: Total tokens processed
        """
        import io
        import sys
        import re
        from contextlib import redirect_stdout

        try:
            # Capture stdout
            f = io.StringIO()
            with redirect_stdout(f):
                self.llm._ctx.print_timings()
            output = f.getvalue()
            
            logger.debug(f"Timing output: {output}")
            
            # Parse the output using regex
            stats = {}
            
            # Load time
            load_match = re.search(r'load time\s*=\s*(\d+\.\d+)\s*ms', output)
            if load_match:
                stats['load_time_ms'] = float(load_match.group(1))
            
            # Prompt eval time and tokens
            prompt_match = re.search(r'prompt eval time\s*=\s*(\d+\.\d+)\s*ms\s*/\s*(\d+)\s*tokens', output)
            if prompt_match:
                stats['prompt_eval_time_ms'] = float(prompt_match.group(1))
                stats['prompt_tokens'] = int(prompt_match.group(2))
                if stats['prompt_eval_time_ms'] > 0:
                    stats['prompt_tokens_per_second'] = 1e3 / stats['prompt_eval_time_ms'] * stats['prompt_tokens']
                else:
                    stats['prompt_tokens_per_second'] = 0.0
            
            # Eval time and tokens
            eval_match = re.search(r'eval time\s*=\s*(\d+\.\d+)\s*ms\s*/\s*(\d+)\s*runs', output)
            if eval_match:
                stats['eval_time_ms'] = float(eval_match.group(1))
                stats['eval_tokens'] = int(eval_match.group(2))
                if stats['eval_time_ms'] > 0:
                    stats['eval_tokens_per_second'] = 1e3 / stats['eval_time_ms'] * stats['eval_tokens']
                else:
                    stats['eval_tokens_per_second'] = 0.0
            
            # Total time and tokens
            total_match = re.search(r'total time\s*=\s*(\d+\.\d+)\s*ms\s*/\s*(\d+)\s*tokens', output)
            if total_match:
                stats['total_time_ms'] = float(total_match.group(1))
                stats['total_tokens'] = int(total_match.group(2))
            else:
                # Calculate totals if not found in output
                stats['total_time_ms'] = stats.get('prompt_eval_time_ms', 0.0) + stats.get('eval_time_ms', 0.0)
                stats['total_tokens'] = stats.get('prompt_tokens', 0) + stats.get('eval_tokens', 0)
            
            logger.debug(f"Parsed stats: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Error accessing timing statistics: {e}")
            return {}