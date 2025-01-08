from sanic import Sanic, json
from nano_llm import NanoLLM
import asyncio
import json
import time
    
app = Sanic("nanollm_server")
app.config.MODEL_PATH

@app.before_server_start
async def setup_model(app):
    app.ctx.model = NanoLLM(model_path=app.config.MODEL_PATH)

@app.post("/v1/chat/completions")
async def chat_completions(request):

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
            response = await asyncio.to_thread(
                request.app.ctx.model.generate,
                prompt,
                max_tokens=data.get("max_tokens", 100),
                temperature=data.get("temperature", 0.7)
            )
            
            completion_response = {
                "id": "chatcmpl-" + str(hash(response))[:8],
                "object": "chat.completion",
                "created": int(time.time()),
                "model": "nanollm",
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response
                    },
                    "finish_reason": "stop"
                }],
                "usage": {
                    "prompt_tokens": len(prompt.split()),
                    "completion_tokens": len(response.split()),
                    "total_tokens": len(prompt.split()) + len(response.split())
                }
            }
            
            return json(completion_response)
        
        # Reponse with streaming
        else:
        
            chunk_id = f"chatcmpl-{str(hash(prompt))[:8]}"

            response.headers["Content-Type"] = "text/event-stream"
            response.headers["Cache-Control"] = "no-cache"
            response.headers["Connection"] = "keep-alive"
            
            async for token in request.app.ctx.model.generate_stream(
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
            
            response.send(f"data: {json.dumps(final_chunk)}\n\n")
            response.send("data: [DONE]\n\n")
    
    except Exception as e:
        return json({"error": str(e)}, status=500)

