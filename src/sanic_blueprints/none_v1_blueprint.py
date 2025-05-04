import json
from sanic import Blueprint
from sanic.response import json as response_json

from src.utils.logger import logger


none_v1_bp = Blueprint('none', url_prefix = '/v1')


@none_v1_bp.post("/none")
async def get_embeddings(request):
    app = request.app
    data = request.json
    messages = data.get("messages", [])
   
    try:

        usage: dict = {}
        choices: dict = {}

        response_from_llm: str = await app.ctx.model.generate(
            messages,
            max_tokens=data.get("max_tokens", 100),
            temperature=data.get("temperature", 0.7)
        )
        
        completion_response = {
           "response": response_from_llm
        }

        logger.info(f'Response: {completion_response}')
        
        return response_json(completion_response)
    
    except Exception as e:

        return response_json({"error": str(e)}, status=500)
    