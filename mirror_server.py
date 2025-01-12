from src.model_adapter import ModelAdapter
from src.model_port_mirror import MirrorModel
from src.sanic_server import create_server


mirror_model: ModelAdapter = MirrorModel()

app = create_server(mirror_model)