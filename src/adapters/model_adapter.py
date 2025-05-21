from abc import ABC


class ModelAdapter(ABC):

    name: str
    model_local_path_for_tokenizer: str|None
    
    async def generate_chat(self, messages, max_tokens=100, temperature=0.7):
        pass

    async def generate_chat_stream(self, messages, max_tokens=100, temperature=0.7):
        pass

    async def generate(self, prompt, max_tokens=100, temperature=0.7):
        pass

    async def generate_stream(self, prompt, max_tokens=100, temperature=0.7):
        pass

    def count_nb_tokens(self, text, model_local_path_for_tokenizer):
        pass

    def close(self):
        pass