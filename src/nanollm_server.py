from sanic import Sanic, json
from sanic.response import StreamingHTTPResponse
from nanollm import NanoLLM
import asyncio
import json
import time

def create_app(model_path: str = "path/to/your/model") -> Sanic:
    app = Sanic("nanollm_server")

    @app.before_server_start
    async def setup_model(app, loop):
        app.ctx.model = NanoLLM(model_path=model_path)

    @app.post("/v1/chat/completions")
    async def chat_completions(request):
        try:
            data = request.json
            messages = data.get("messages", [])
            stream = data.get("stream", False)
            
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
            
            async def stream_response():
                chunk_id = f"chatcmpl-{str(hash(prompt))[:8]}"
                
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
                    yield f"data: {json.dumps(chunk)}\n\n"
                
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
                yield f"data: {json.dumps(final_chunk)}\n\n"
                yield "data: [DONE]\n\n"
        
            return StreamingHTTPResponse(
                stream_response(),
                headers={
                    "Content-Type": "text/event-stream",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                }
            )
        
        except Exception as e:
            return json({"error": str(e)}, status=500)

    return app
