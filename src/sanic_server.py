from sanic import Sanic

from src.model_adapter import ModelAdapter
from src.openai_v1_blueprint import openai_v1_bp


def create_server(model_adapter: ModelAdapter) -> Sanic:
    
    app = Sanic(model_adapter.name)
    bp = openai_v1_bp
    app.blueprint(bp)

    # Set mock model in app context
    @app.before_server_start
    async def setup_mock(app, loop):
        app.ctx.model = model_adapter

   

    return app