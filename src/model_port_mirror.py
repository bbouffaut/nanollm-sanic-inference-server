# Load mock data
import asyncio
import json

from src.model_adapter import ModelAdapter


with open('./src/mock_responses.json', 'r') as f:
    MOCK_DATA = json.load(f)

async def mirror_generate(prompt):
    return prompt

async def mirror_generate_stream(prompt):
    # Split into tokens (words for this example)
    tokens = prompt.split()
    for token in tokens:
        await asyncio.sleep(0.1)  # Simulate generation delay
        yield token + " "

# Replace the model with mock functions
class MirrorModel(ModelAdapter):

    name: str = "MockModel"

    async def generate(self, prompt, max_tokens=100, temperature=0.7):
        return await mirror_generate(prompt)
    
    async def generate_stream(self, prompt, max_tokens=100, temperature=0.7):
        async for token in mirror_generate_stream(prompt):
            yield token