import json
import time
from sanic import Blueprint
from sanic.response import json as response_json


openai_v1_bp = Blueprint('openai', url_prefix = '/v1')

def count_messages_total_tokens(messages):
    # This is a simple implementation and may not be accurate for all cases.
    # For more accurate token counting, consider using a tokenizer library.
    return sum([len(msg.get("content", "").split()) for msg in messages])

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
    prompt_tokens = count_messages_total_tokens(messages)

    if not stream:
        try:
            response_from_llm = await app.ctx.model.generate(
                messages,
                max_tokens=data.get("max_tokens", 100),
                temperature=data.get("temperature", 0.7)
            )

            if isinstance(response_from_llm, dict):
                content = response_from_llm.get('content', '')
                usage = response_from_llm.get('usage', {
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": len(content.split()),
                    "total_tokens": prompt_tokens + len(content.split())
                })
                choices = response_from_llm.get('choices', [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": content
                    },
                    "finish_reason": "stop"
                }])
            else:
                content = response_from_llm
                completion_tokens = len(content.split())
                usage = {
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": prompt_tokens + completion_tokens
                }
                choices = [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": content
                    },
                    "finish_reason": "stop"
                }]
            
            completion_response = {
                "id": "chatcmpl-" + str(hash(content))[:8],
                "object": "chat.completion",
                "created": int(time.time()),
                "model": "nanollm",
                "choices": choices,
                "usage": usage
            }

            print(f'Response: {completion_response}')
            
            return response_json(completion_response)
        except Exception as e:
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