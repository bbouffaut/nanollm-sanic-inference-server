import json
from sanic import Sanic
from src.params.model_info_type import ModelInfo
from src.services.sanic_server import create_server
from src.utils.logger import logger
from src.utils.constants import MODELS_PARAMS_FILE

def get_model_info_from_id(params_id: str) -> ModelInfo:

    logger.debug(f'Loading model parameters from {MODELS_PARAMS_FILE}')
    
    with open(MODELS_PARAMS_FILE, 'r') as file:
        models_params = json.load(file)
    
    if params_id in models_params:
        return ModelInfo(**models_params[params_id])  # Assuming ModelInfo can be initialized with a dict
    else:
        raise KeyError(f"Model parameters for '{params_id}' not found.")


def create_app(params_id: str) -> Sanic:

    params: ModelInfo = get_model_info_from_id(params_id)
    logger.info(f"Creating app with ModelInfo: {json.dumps(params.__dict__)}")

    app = create_server(params)

    return app