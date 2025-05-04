from src.params.models_classes import MODEL_CLASSES
from src.adapters.model_adapter import ModelAdapter
from src.params.model_info_type import ModelInfo
from src.utils.logger import logger


def create_model_instance(model_info: ModelInfo) -> ModelAdapter:
    """
    Create an instance of the model based on the provided model_info.

    :param model_info: An object containing 'name' and 'params' for the model.
    :return: An instance of ModelAdapter.
    """
    model_name = model_info.name
    model_params = model_info.params

    model_class = MODEL_CLASSES.get(model_name)
    if model_class is None:
        logger.error(f"Model '{model_name}' is not supported.")
        raise ValueError(f"Model '{model_name}' is not supported.")

    logger.info(f"Creating model instance for {model_name} with params: {model_params}")
    return model_class(**model_params)