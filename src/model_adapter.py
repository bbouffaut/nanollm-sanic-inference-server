from abc import ABC


class ModelAdapter(ABC):

    name: str
    
    async def generate(self, messages, max_tokens=100, temperature=0.7):
        pass

    async def generate_stream(self, messages, max_tokens=100, temperature=0.7):
        pass