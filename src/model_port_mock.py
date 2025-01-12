# Load mock data
import asyncio
import json

from src.model_adapter import ModelAdapter


with open('./src/mock_responses.json', 'r') as f:
    MOCK_DATA = json.load(f)

async def mock_generate():
    return MOCK_DATA["regular_response"]

async def mock_generate_stream():
    stream_text = MOCK_DATA["stream_response"]
    # Split into tokens (words for this example)
    tokens = stream_text.split()
    for token in tokens:
        await asyncio.sleep(0.1)  # Simulate generation delay
        yield token + " "

# Replace the model with mock functions
class MockModel(ModelAdapter):

    name: str = "MockModel"

    async def generate(self, messages, max_tokens=100, temperature=0.7):
        return await mock_generate()
    
    async def generate_stream(self, messages, max_tokens=100, temperature=0.7):
        async for token in mock_generate_stream():
            yield token