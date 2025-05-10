
from src.adapters.model_adapter import ModelAdapter
from src.utils.logger import logger
from nano_llm import NanoLLM


def nanollm_generate(messages, llm, temperature):
    response = llm.generate(
        inputs=messages,
        temperature=temperature,
        streaming=False
    )
    print(f'Response: {response}')
    return response
    

async def nanollm_generate_stream(messages, llm, temperature):
    response = llm.generate(
        inputs=messages,
        temperature=temperature,
        streaming=True
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
class NanoLlmModel(ModelAdapter):

    name: str = "NanoLlmModel"
    has_arguments: bool = True

    def __init__(self, model_path: str, gpu: bool, api: str = 'hf'):
        # import traceback
        logger.info(f"Initialized NanoLlm with model path: {model_path} and gpu: {gpu}")
        self.llm = NanoLLM.from_pretrained(
            model=model_path,
            api=api,                   # supported APIs are: mlc, awq, hf
        )
       # traceback.print_stack()  # Show where it's being called from

    async def generate(self, messages, max_tokens=100, temperature=0.7):
        return nanollm_generate(messages, self.llm, temperature)
    
    async def generate_stream(self, messages, max_tokens=100, temperature=0.7):
        async for chunk in nanollm_generate_stream(messages, self.llm, temperature):
            yield chunk