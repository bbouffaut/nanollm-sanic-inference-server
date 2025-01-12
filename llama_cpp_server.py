from src.model_adapter import ModelAdapter
from src.model_port_llama_cpp import LlamaCppModel
from src.sanic_server import create_server


llama_cpp_model: ModelAdapter = LlamaCppModel()

app = create_server(llama_cpp_model)