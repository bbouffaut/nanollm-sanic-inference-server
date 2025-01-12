from src.model_adapter import ModelAdapter
from src.model_port_echo import EchoModel
from src.sanic_server import create_server


echo_model: ModelAdapter = EchoModel()

app = create_server(echo_model)