from sanic import Sanic

from src.adapters.model_adapter import ModelAdapter
from src.services.openai_v1_blueprint import openai_v1_bp
from src.utils.constants import SERVER_PORT


def create_server(model_adapter: ModelAdapter) -> Sanic:
    
    app = Sanic(model_adapter.name)
    # app.prepare(port=SERVER_PORT)
    bp = openai_v1_bp
    app.blueprint(bp)

    # Set mock model in app context
    @app.before_server_start
    async def setup_model(app):
        app.ctx.model = model_adapter

    return app