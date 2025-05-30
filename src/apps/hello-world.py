from sanic import Sanic
from sanic.response import text
from src.utils.constants import PORT

app = Sanic("MyHelloWorldApp")

@app.get("/")
async def hello_world(request):
    return text("Hello, world.")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=False, access_log=False, workers=1)