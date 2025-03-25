import argparse
import os
from pathlib import Path

from src.adapters.model_adapter import ModelAdapter
from src.ports.model_port_llama_cpp import LlamaCppModel
from src.services.sanic_server import create_server
from src.utils.constants import MODEL_PATH


def llama_cpp_server():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Launch LlamaCpp model server')
    parser.add_argument('--model', type=str, help='Name of the model file to use', required=True)
    args = parser.parse_args()

    # Set model path
    model_file_path = os.path.join(MODEL_PATH, args.model)
    
    # Ensure the model file exists
    if not Path(model_file_path).exists():
        print(f"Error: Model file not found at {model_file_path}")
        exit(1)
    
    # Initialize the model with the specified path
    llama_cpp_model: ModelAdapter = LlamaCppModel(model_path=model_file_path)
    
    # Create and return the Sanic app
    app = create_server(llama_cpp_model)
    return app


app = llama_cpp_server()
