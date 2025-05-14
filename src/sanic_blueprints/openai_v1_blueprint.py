import json
import time
from sanic import Blueprint
from sanic.response import json as response_json

from src.utils.logger import logger
from src.services.openai_services import compute_usage_from_dict, compute_usage_from_text


openai_v1_bp = Blueprint('openai', url_prefix = '/v1')

def compute_message_hash(messages):
    # Convert messages to string and hash it
    message_str = ''.join([msg.get("content", "") for msg in messages])
    hash_value = str(hash(message_str))[:8]
    return hash_value


@openai_v1_bp.post("/chat/completions")
async def chat_completions(request):
    app = request.app
    data = request.json
    messages = data.get("messages", [])
    stream = data.get("stream", False)
    include_usage = data.get("include_usage", False)
    response_from_llm = {}
   
    # Process non-streaming response
    if not stream:

        try:

            usage: dict = {}
            choices: dict = {}

            response_from_llm = await app.ctx.model.generate(
                messages,
                max_tokens=data.get("max_tokens", 100),
                temperature=data.get("temperature", 0.7)
            )

            if isinstance(response_from_llm, dict):

                choices = response_from_llm.get('choices')
                logger.debug(f'Response is Dict with choices = {choices}')

                if include_usage:

                    usage = compute_usage_from_dict(
                        messages,
                        response_from_llm,
                        app.ctx.model
                    )
            
            else:
                
                if include_usage:

                    usage = compute_usage_from_text(
                        messages,
                        response_from_llm,
                        app.ctx.model
                    )
                
                choices = [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response_from_llm
                    },
                    "finish_reason": "stop"
                }]
            
            completion_response = {
                "id": "chatcmpl-" + compute_message_hash(messages),
                "object": "chat.completion",
                "created": int(time.time()),
                "model": "nanollm",
                "choices": choices,
                "usage": usage
            }

            logger.info(f'Response: {completion_response}')
            return response_json(completion_response)
        
        except Exception as e:

            logger.error(f'An Error happened processing {response_from_llm}: {str(e)}')
            return response_json({"error": str(e)}, status=500)
    
    # Streaming response
    response = await request.respond(content_type="text/event-stream")
    chunk_id = f"chatcmpl-{compute_message_hash(messages)}"
    
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Connection"] = "keep-alive"
    
    try:
        async for token in app.ctx.model.generate_stream(
            messages,
            max_tokens=data.get("max_tokens", 100),
            temperature=data.get("temperature", 0.7)
        ):
            if isinstance(token, dict):
                if token.get('choices', [{}])[0].get('finish_reason') is not None:
                    continue
                chunk = token
            else:
                chunk = {
                    "id": chunk_id,
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": "nanollm",
                    "choices": [{
                        "index": 0,
                        "delta": {
                            "role": "assistant",
                            "content": token
                        },
                        "finish_reason": None
                    }]
                }
            
            await response.send(f"data: {json.dumps(chunk)}\n\n")
        
        final_chunk = {
            "id": chunk_id,
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": "nanollm",
            "choices": [{
                "index": 0,
                "delta": {},
                "finish_reason": "stop"
            }]
        }
        
        await response.send(f"data: {json.dumps(final_chunk)}\n\n")
        await response.send("data: [DONE]\n\n")
    
    except Exception as e:
        await response.send(f"data: {json.dumps({'error': str(e)})}\n\n")
    
    finally:
        await response.eof()