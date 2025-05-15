from typing import List, Optional
from sanic import Blueprint

from src.adapters.openai.openai_api_protocol import LogProbsContent
from src.services.openai_services import wrap_chat_completion_response
from src.utils.utils import random_uuid


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
    request_id = f"chatcmpl-{random_uuid()}"

    response_from_llm = await app.ctx.model.generate(
        messages,
        max_tokens=data.get("max_tokens", 100),
        temperature=data.get("temperature", 0.7)
    )
   
    if stream:

        first_response = await anext(  # type: ignore  # pylint: disable=undefined-variable
            response_from_llm
        )
        # Streaming response
        response = await request.respond(content_type="text/event-stream")
        
        response.headers["Cache-Control"] = "no-cache"
        response.headers["Connection"] = "keep-alive"

        if isinstance(first_response, StopAsyncIteration):
            await response.send("data: [DONE]\n\n")
        await response.send(f"data: {first_response.model_dump_json(by_alias=True)}\n\n")
        async for response in response_from_llm:
            await response.send(f"data: {response.model_dump_json(by_alias=True)}\n\n")
        await response.send("data: [DONE]\n\n")

    
    # Streaming response
    response = await request.respond(content_type="text/event-stream")
    
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Connection"] = "keep-alive"
    
    # Normal response.
    request_final_usage = None
    output_texts = [""]
    finish_reasons: List[Optional[str]] = [None]

    # usage is always the last chunk
    if response_from_llm.usage is not None:
        request_final_usage = response_from_llm.usage

    for choice in response_from_llm.choices:
        assert isinstance(choice.delta.content, str)
        output_texts[choice.index] += choice.delta.content
        if choice.finish_reason is not None and finish_reasons[choice.index] is None:
            finish_reasons[choice.index] = choice.finish_reason

    assert all(finish_reason is not None for finish_reason in finish_reasons)

    return wrap_chat_completion_response(
        request_id=request_id,
        model=request.model,
        output_texts=output_texts,
        finish_reasons=finish_reasons,
        usage=request_final_usage,
    )