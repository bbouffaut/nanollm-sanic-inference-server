from src.adapters.model_adapter import ModelAdapter
from src.ports.model_port_echo import EchoModel
from src.services.sanic_server import create_server
from src.utils.constants import LOGGING_LEVEL, SERVER_PORT


echo_model: ModelAdapter = EchoModel()

app = create_server(echo_model)

# app.run(host="0.0.0.0", port=SERVER_PORT, debug=(LOGGING_LEVEL == "DEBUG"))