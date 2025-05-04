import json
from sanic import Sanic
from src.params.model_info_type import ModelInfo
from src.services.sanic_server import create_server
from src.utils.constants import MODELS_PARAMS_FILE

def get_model_info_from_name(params_name: str) -> ModelInfo:
    with open(MODELS_PARAMS_FILE, 'r') as file:
        models_params = json.load(file)
    
    if params_name in models_params:
        return ModelInfo(**models_params[params_name])  # Assuming ModelInfo can be initialized with a dict
    else:
        raise KeyError(f"Model parameters for '{params_name}' not found.")


def create_app_from_params_nanme(params_name: str) -> Sanic:

    params: ModelInfo = get_model_info_from_name(params_name)

    app = create_server(params)

    return app