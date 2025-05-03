import argparse
import os
from pathlib import Path

from sanic import Sanic

from src.adapters.model_adapter import ModelAdapter
from src.ports.model_port_llama_cpp import LlamaCppModel
from src.services.sanic_server import create_server
from src.utils.constants import LOGGING_LEVEL, MODEL_PATH, SERVER_PORT


def create_app(model_path: str) -> Sanic:

    # Set model path
    model_file_path = os.path.join(MODEL_PATH, model_path)
    
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
    parser = argparse.ArgumentParser(description="LLaMA CPP Server")
    parser.add_argument("--model_path", type=str, help="Path to the model file")
    args = parser.parse_args()

    app = create_app(args.model_path)
    return app

app = main()

# app.run(host="0.0.0.0", port=SERVER_PORT, debug=(LOGGING_LEVEL == "DEBUG"))