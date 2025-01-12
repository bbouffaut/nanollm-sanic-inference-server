# Load mock data
import asyncio
import json

from src.model_adapter import ModelAdapter


with open('./src/mock_responses.json', 'r') as f:
    MOCK_DATA = json.load(f)

async def mirror_generate(prompt):
    return f'Voici le prompt reçu :\n {prompt}'

async def mirror_generate_stream(prompt):
    # Split into tokens (words for this example)
    prompt = f'Voici le prompt reçu :\n {prompt}'
    tokens = prompt.split()
    for token in tokens:
        yield token + " "

def generate_prompt(messages):
    prompt = ""
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        prompt += f"{role}: {content}\n"
    return prompt
# Replace the model with mock functions
class EchoModel(ModelAdapter):

    name: str = "EchoModel"

    async def generate(self, messages, max_tokens=100, temperature=0.7):
        return await mirror_generate(generate_prompt(messages))
    
    async def generate_stream(self, messages, max_tokens=100, temperature=0.7):
        async for token in mirror_generate_stream(generate_prompt(messages)):
            yield token