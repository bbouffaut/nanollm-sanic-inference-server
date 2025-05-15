from sanic import Sanic
from sanic.worker.manager import WorkerManager

from src.types.models_classes import MODEL_TYPES
from src.ports.models_port_generator import create_model_instance
from src.types.model_info_type import ModelInfo
from src.adapters.model_adapter import ModelAdapter
from src.sanic_blueprints.openai_v1_blueprint import openai_v1_bp
from src.sanic_blueprints.embeddings_v1_blueprint import embeddings_v1_bp
from src.sanic_blueprints.none_v1_blueprint import none_v1_bp
from src.utils.constants import SANIC_WORKER_STARTUP_THRESHOLD
from src.utils.logger import logger


def create_server(model_info: ModelInfo) -> Sanic:

    logger.info(f"Creating server with name: {model_info.name}")
    
    app = Sanic(name=model_info.name)

    if (model_info.type == MODEL_TYPES.CHAT_COMPLETION):
        bp = openai_v1_bp
    elif (model_info.type == MODEL_TYPES.EMBEDDINGS):
        bp = embeddings_v1_bp
    else:
        bp = none_v1_bp

    
    app.blueprint(bp)

    WorkerManager.THRESHOLD = SANIC_WORKER_STARTUP_THRESHOLD

    # Set mock model in app context
    @app.after_server_start
    async def after_server_start(app):
        
        # Initialize the model with the specified path
        logger.info(f"Worker Thread start thread with model_info {model_info}")
        model_port: ModelAdapter = create_model_instance(model_info)
        app.ctx.model = model_port

    
    @app.after_server_stop
    async def after_server_stop(app):
        logger.info(f"Worker Stop thread with app.ctx {app.ctx.model.name}")

        if hasattr(app.ctx.model, 'close'):
            app.ctx.model.close()

    return app