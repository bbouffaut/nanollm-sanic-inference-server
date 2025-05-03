
from sanic import Sanic
from src.services.sanic_server import create_server


def main() -> Sanic:

    app = create_server()
    return app

app = main()