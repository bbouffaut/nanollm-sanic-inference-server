
from llama_cpp import Llama
from src.constants import MODEL_PATH
from src.model_adapter import ModelAdapter


def llama_cpp_generate(messages, llm, temperature):
    response = llm.create_chat_completion(
        messages=messages,
        response_format={
            "type": "json_object",
            "schema": {
                "type": "object",
                "properties": {"team_name": {"type": "string"}},
                "required": ["team_name"],
            },
        },
        temperature=temperature,
    )
    print(f'Response: {response}')
    return response
    

async def mirror_generate_stream(prompt, llm):
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
class LlamaCppModel(ModelAdapter):

    name: str = "EchoModel"

    def __init__(self):
        self.llm = Llama(model_path=MODEL_PATH, chat_format="chatml")

    async def generate(self, messages, max_tokens=100, temperature=0.7):
        return llama_cpp_generate(messages, self.llm, temperature)
    
    async def generate_stream(self, messages, max_tokens=100, temperature=0.7):
        async for token in mirror_generate_stream(generate_prompt(messages)):
            yield token