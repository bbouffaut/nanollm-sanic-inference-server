from src.adapters.model_adapter import ModelAdapter
from src.ports.model_port_echo import EchoModel
from src.services.sanic_server import create_server


echo_model: ModelAdapter = EchoModel()

app = create_server(echo_model)