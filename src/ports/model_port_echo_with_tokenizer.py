from src.adapters.model_adapter import ModelAdapter
from src.services.openai_services import generate_prompt_text_from_messages


async def mirror_generate(prompt):
    return f'Voici le prompt reçu :\n {prompt}'

async def mirror_generate_stream(prompt):
    # Split into tokens (words for this example)
    prompt = f'Voici le prompt reçu :\n {prompt}'
    tokens = prompt.split()
    for token in tokens:
        yield token + " "

# Replace the model with mock functions
class EchoModelWithTokenizer(ModelAdapter):

    name: str = "EchoModel"

    async def generate(self, messages, max_tokens=100, temperature=0.7):
        return await mirror_generate(generate_prompt_text_from_messages(messages))
    
    async def generate_stream(self, messages, max_tokens=100, temperature=0.7):
        async for token in mirror_generate_stream(generate_prompt_text_from_messages(messages)):
            yield token