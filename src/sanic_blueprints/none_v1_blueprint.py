import json
from sanic import Blueprint
from sanic.response import json as response_json

from src.utils.logger import logger


none_v1_bp = Blueprint('none', url_prefix = '/v1')


@none_v1_bp.post("/none")
async def get_embeddings(request):
    app = request.app
    data = request.json

   
    try:
        response = await request.respond(content_type="json")

        await response.send("data: [DONE]\n\n")
    
    except Exception as e:
        await response.send(f"data: {json.dumps({'error': str(e)})}\n\n")
    
    finally:
        await response.eof()