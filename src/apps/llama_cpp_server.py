import os
from pathlib import Path

from sanic import Sanic

from src.adapters.model_adapter import ModelAdapter
from src.ports.model_port_llama_cpp import LlamaCppModel
from src.services.sanic_server import create_server
from src.utils.constants import MODEL_FILE, MODEL_PATH


def create_app(model_file_path: str) -> Sanic:
    
    # Ensure the model file exists
    if not Path(model_file_path).exists():
        print(f"Error: Model file not found at {model_file_path}")
        exit(1)
    
    # Initialize the model with the specified path
    llama_cpp_model: ModelAdapter = LlamaCppModel(model_path=model_file_path)
    
    # Create and return the Sanic app
    app = create_server(llama_cpp_model)
    return app

def main():

 # Set model path
    model_file_path = os.path.join(MODEL_PATH, MODEL_FILE)

    app = create_app(model_file_path)
    return app

app = main()