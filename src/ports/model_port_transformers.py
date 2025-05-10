
from threading import Thread
from src.adapters.model_adapter import ModelAdapter
from src.utils.logger import logger
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer


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
    

def generate_prompt(messages):
    prompt = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        prompt.append({f"{role}: {content}"})
    return prompt
# Replace the model with mock functions
class TransformersModel(ModelAdapter):

    name: str = "LlamaCppModel"
    has_arguments: bool = True

    def __init__(self, model_path: str, gpu: bool):
        device_map = 'cuda' if gpu else 'cpu'
        self.model = AutoModelForCausalLM.from_pretrained(model_path, device_map=device_map)

        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.streamer = TextIteratorStreamer(self.tokenizer)      

    async def generate_stream(self, messages, max_tokens=100):
        prompt = generate_prompt(messages)
        inputs = self.tokenizer.apply_chat_template(
            prompt,
            add_generation_prompt=True,
            return_tensors='pt'
        ).to(self.model.device)

        Thread(target=lambda: self.model.generate(inputs, max_new_tokens=max_tokens, streamer=self.streamer)).start()

        for text in self.streamer:
            yield text
        
    
    async def generate(self, messages, max_tokens=100):
        prompt = generate_prompt(messages)
        inputs = self.tokenizer.apply_chat_template(
            prompt,
            add_generation_prompt=True,
            return_tensors='pt'
        ).to(self.model.device)

        response = self.model.generate(inputs, max_new_tokens=max_tokens)
        return response

        