import json
import time
from sanic import Blueprint
from sanic.response import json as response_json

from src.utils.logger import logger


embeddings_v1_bp = Blueprint('embeddings', url_prefix = '/v1')


@embeddings_v1_bp.post("/embeddings")
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