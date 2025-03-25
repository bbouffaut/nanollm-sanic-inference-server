from src.adapters.model_adapter import ModelAdapter
from src.ports.model_port_mock import MockModel
from src.services.sanic_server import create_server


mock_model: ModelAdapter = MockModel()

app = create_server(mock_model)