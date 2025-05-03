from src.adapters.model_adapter import ModelAdapter
from src.ports.model_port_echo_with_tokenizer import EchoModelWithTokenizer
from src.services.sanic_server import create_server


echo_model: ModelAdapter = EchoModelWithTokenizer()

app = create_server(echo_model)