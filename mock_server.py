from src.model_adapter import ModelAdapter
from src.model_port_mock import MockModel
from src.sanic_server import create_server


mock_model: ModelAdapter = MockModel()

app = create_server(mock_model)