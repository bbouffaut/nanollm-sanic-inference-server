from src.model_adapter import ModelAdapter
from src.model_port_echo_with_tokenizer import EchoModelWithTokenizer
from src.sanic_server import create_server


echo_model: ModelAdapter = EchoModelWithTokenizer()

app = create_server(echo_model)