from abc import ABC


class ModelAdapter(ABC):

    name: str
    
    async def generate(self, prompt, max_tokens=100, temperature=0.7):
        pass

    async def generate_stream(self, prompt, max_tokens=100, temperature=0.7):
        pass