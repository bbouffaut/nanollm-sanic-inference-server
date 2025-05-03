import os
from pathlib import Path
from sanic import Sanic

from src.adapters.model_adapter import ModelAdapter
from src.ports.model_port_llama_cpp import LlamaCppModel
from src.services.openai_v1_blueprint import openai_v1_bp
from src.utils.logger import logger
from src.utils.constants import MODEL_FILE, MODEL_PATH


def create_name(model_file_path):
    # Get the file name from the model file path
    file_name = os.path.basename(model_file_path)
    # Remove the file extension
    file_name = os.path.splitext(file_name)[0]
    # Replace spaces with underscores
    file_name = file_name.replace(" ", "_")
    return file_name

def create_server() -> Sanic:

    model_file_path = os.path.join(MODEL_PATH, MODEL_FILE)
    # Ensure the model file exists
    if not Path(model_file_path).exists():
        logger.error(f"Error: Model file not found at {model_file_path}")
        exit(1)

    name = create_name(model_file_path)
    logger.info(f"Creating server with name: {name}")
    
    app = Sanic(name=name)
    bp = openai_v1_bp
    app.blueprint(bp)

    # Set mock model in app context
    @app.before_server_start
    async def setup_model(app):
        
        
        # Initialize the model with the specified path
        llama_cpp_model: ModelAdapter = LlamaCppModel(model_path=model_file_path)
        app.ctx.model = llama_cpp_model

    return app