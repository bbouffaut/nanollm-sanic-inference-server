import json
import time
from typing import Any, AsyncGenerator, List, Optional
from sanic import Blueprint
from sanic.response import json as response_json

from src.services.openai_services import wrap_chat_completion_response, wrap_completion_response
from src.utils.logger import logger
from src.utils.utils import random_uuid
from src.adapters.openai.openai_api_protocol import ChatCompletionResponse, ChatCompletionStreamResponse, CompletionResponse, CompletionUsage



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
    request_id = f"chatcmpl-{random_uuid()}"
    start_time = time.time()
   
    if stream:
        response_from_llm: AsyncGenerator[ChatCompletionResponse, Any] = app.ctx.model.generate_chat_stream(
            messages,
            max_tokens=data.get("max_tokens", 100),
            temperature=data.get("temperature", 0.7)
        )

        first_response: ChatCompletionResponse = await anext(  # type: ignore  # pylint: disable=undefined-variable
            response_from_llm
        )

        logger.debug(f"first_response = {first_response}")
        
        # Streaming response
        response = await request.respond(content_type="text/event-stream")
        
        response.headers["Cache-Control"] = "no-cache"
        response.headers["Connection"] = "keep-alive"

        if isinstance(first_response, StopAsyncIteration):
            await response.send("data: [DONE]\n\n")
        await response.send(f"data: {first_response.model_dump_json(by_alias=True)}\n\n")
        
        async for response_chunk in response_from_llm:
            await response.send(f"data: {response_chunk.model_dump_json(by_alias=True)}\n\n")
        
        # Add timing information in the final [DONE] message
        processing_time = time.time() - start_time
        final_usage = {
            "prompt_tokens": 0,  # These will be filled by the model if available
            "completion_tokens": 0,
            "total_tokens": 0,
            "extra": {
                "processing_time_seconds": round(processing_time, 3)
            }
        }
        final_response = {
            "data": "[DONE]",
            "usage": final_usage
        }
        await response.send(f"data: {json.dumps(final_response)}\n\n")
        return

    
    # Non Streaming response
    response_from_llm: ChatCompletionStreamResponse = await app.ctx.model.generate_chat(
        messages,
        max_tokens=data.get("max_tokens", 100),
        temperature=data.get("temperature", 0.7)
    )

    # Normal response.
    request_final_usage = None
    output_texts = [""]
    finish_reasons: List[Optional[str]] = [None]

    # usage is always the last chunk
    if hasattr(response_from_llm, 'usage') and response_from_llm.usage is not None:
        request_final_usage: CompletionUsage = response_from_llm.usage
        if request_final_usage.extra is None:
            request_final_usage.extra = {}
        request_final_usage.extra["processing_time_seconds"] = round(time.time() - start_time, 3)

    for choice in response_from_llm.choices:
        assert isinstance(choice.message.content, str)
        output_texts[choice.index] += choice.message.content
        if choice.finish_reason is not None and finish_reasons[choice.index] is None:
            finish_reasons[choice.index] = choice.finish_reason

    assert all(finish_reason is not None for finish_reason in finish_reasons)

    completion_response: ChatCompletionResponse = wrap_chat_completion_response(
        request_id=request_id,
        model=app.ctx.model.name,
        output_texts=output_texts,
        finish_reasons=finish_reasons,
        usage=request_final_usage,
    )

    return response_json(json.loads(completion_response.model_dump_json(by_alias=True)))

@openai_v1_bp.post("/completions")
async def completions(request):
    app = request.app
    data = request.json
    prompt = data.get("prompt", "")
    stream = data.get("stream", False)
    request_id = f"cmpl-{random_uuid()}"
    start_time = time.time()
   
    if stream:

        response_from_llm: AsyncGenerator[CompletionResponse, Any] = app.ctx.model.generate_stream(
            prompt,
            max_tokens=data.get("max_tokens", 100),
            temperature=data.get("temperature", 0.7)
        )

        first_response: CompletionResponse = await anext(  # type: ignore  # pylint: disable=undefined-variable
            response_from_llm
        )

        logger.debug(f"first_response = {first_response}")
        
        # Streaming response
        response = await request.respond(content_type="text/event-stream")
        
        response.headers["Cache-Control"] = "no-cache"
        response.headers["Connection"] = "keep-alive"

        if isinstance(first_response, StopAsyncIteration):
            await response.send("data: [DONE]\n\n")
        await response.send(f"data: {first_response.model_dump_json(by_alias=True)}\n\n")
        
        async for response_chunk in response_from_llm:
            await response.send(f"data: {response_chunk.model_dump_json(by_alias=True)}\n\n")
        
        # Add timing information in the final [DONE] message
        processing_time = time.time() - start_time
        final_usage = {
            "prompt_tokens": 0,  # These will be filled by the model if available
            "completion_tokens": 0,
            "total_tokens": 0,
            "extra": {
                "processing_time_seconds": round(processing_time, 3)
            }
        }
        final_response = {
            "data": "[DONE]",
            "usage": final_usage
        }
        await response.send(f"data: {json.dumps(final_response)}\n\n")
        return

    
    # Non Streaming response
    response_from_llm: CompletionResponse = await app.ctx.model.generate(
        prompt,
        max_tokens=data.get("max_tokens", 100),
        temperature=data.get("temperature", 0.7)
    )

    # Normal response.
    request_final_usage = None
    output_texts = [""]
    finish_reasons: List[Optional[str]] = [None]

    # usage is always the last chunk
    if hasattr(response_from_llm, 'usage') and response_from_llm.usage is not None:
        request_final_usage: CompletionUsage = response_from_llm.usage
        if request_final_usage.extra is None:
            request_final_usage.extra = {}
        request_final_usage.extra["processing_time_seconds"] = round(time.time() - start_time, 3)

    for choice in response_from_llm.choices:
        assert isinstance(choice.text, str)
        output_texts[choice.index] += choice.text
        if choice.finish_reason is not None and finish_reasons[choice.index] is None:
            finish_reasons[choice.index] = choice.finish_reason

    assert all(finish_reason is not None for finish_reason in finish_reasons)

    completion_response: CompletionResponse = wrap_completion_response(
        request_id=request_id,
        model=app.ctx.model.name,
        output_texts=output_texts,
        finish_reasons=finish_reasons,
        usage=request_final_usage
    )

    return response_json(json.loads(completion_response.model_dump_json(by_alias=True)))