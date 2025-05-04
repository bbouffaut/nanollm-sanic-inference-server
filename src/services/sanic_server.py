import os
from pathlib import Path
from sanic import Sanic

from src.ports.models_port_generator import create_model_instance
from src.params.model_info_type import ModelInfo
from src.adapters.model_adapter import ModelAdapter
from src.ports.model_port_llama_cpp import LlamaCppModel
from src.services.openai_v1_blueprint import openai_v1_bp
from src.utils.logger import logger
from src.utils.constants import MODEL_FILE, MODEL_PATH


def create_server(model_info: ModelInfo) -> Sanic:

   

    logger.info(f"Creating server with name: {model_info.name}")
    
    app = Sanic(name=model_info.name)
    bp = openai_v1_bp
    app.blueprint(bp)

    # Set mock model in app context
    @app.before_server_start
    async def setup_model(app):
        
        # Initialize the model with the specified path
        model_port: ModelAdapter = create_model_instance(model_info)
        app.ctx.model = model_port

    return app