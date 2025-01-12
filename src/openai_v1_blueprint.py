import json
import time
from sanic import Blueprint, Sanic


openai_v1_bp = Blueprint('openai', url_prefix = '/v1')

@openai_v1_bp.post("/chat/completions")
async def chat_completions(request):

    app = request.app

    try:
        data = request.json
        messages = data.get("messages", [])
        stream = data.get("stream", False)

        response = await request.respond()
        
        prompt = ""
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            prompt += f"{role}: {content}\n"

        if not stream:
            response_from_llm = await app.ctx.model.generate(
                prompt,
                max_tokens=data.get("max_tokens", 100),
                temperature=data.get("temperature", 0.7)
            )
            
            completion_response = {
                "id": "chatcmpl-" + str(hash(response_from_llm))[:8],
                "object": "chat.completion",
                "created": int(time.time()),
                "model": "nanollm",
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response_from_llm
                    },
                    "finish_reason": "stop"
                }],
                "usage": {
                    "prompt_tokens": len(prompt.split()),
                    "completion_tokens": len(response_from_llm.split()),
                    "total_tokens": len(prompt.split()) + len(response_from_llm.split())
                }
            }

            print(f'Response: {completion_response}')
            
            return response.json(completion_response)
        
        else:
            chunk_id = f"chatcmpl-{str(hash(prompt))[:8]}"

            response.headers["Content-Type"] = "text/event-stream"
            response.headers["Cache-Control"] = "no-cache"
            response.headers["Connection"] = "keep-alive"
            
            async for token in app.ctx.model.generate_stream(
                prompt,
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
        return response.json({"error": str(e)}, status=500)