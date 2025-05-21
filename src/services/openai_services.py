from typing import Any, Dict, List, Optional
from src.adapters.openai.openai_api_protocol import ChatCompletionMessage, ChatCompletionResponse, ChatCompletionResponseChoice, ChatToolCall, CompletionLogProbs, CompletionResponse, CompletionResponseChoice, CompletionUsage, LogProbs, LogProbsContent
from src.utils.logger import logger
from src.adapters.model_adapter import ModelAdapter
from transformers import AutoTokenizer

def generate_prompt_text_from_messages(messages):
    prompt = ""
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        prompt += f"{role}: {content}\n"
    return prompt

def count_tokens_from_text(text: str, model: ModelAdapter|None):
    # This is a simple implementation and may not be accurate for all cases.
    # For more accurate token counting, consider using a tokenizer library.
    if model is None:
        return len(text.split(' '))
    
    else:
        if not hasattr(model, 'model_local_path_for_tokenizer') or model.model_local_path_for_tokenizer is None:
            logger.debug(f'No tokenizer for model {model.name}')
            return len(text.split(' '))
        
        logger.info(f'count_tokens_from_text using tokenizer {model.model_local_path_for_tokenizer}')
        tokenizer = AutoTokenizer.from_pretrained(model.model_local_path_for_tokenizer)
        tokens = tokenizer.encode(text, add_special_tokens=False)
        return len(tokens)
    
def count_tokens_from_messages(messages: dict, model: ModelAdapter|None):
    # This is a simple implementation and may not be accurate for all cases.
    # For more accurate token counting, consider using a tokenizer library.
    prompt = generate_prompt_text_from_messages(messages)
    return count_tokens_from_text(prompt, model)


def compute_usage_from_dict(messages: dict, response_from_llm: dict, model: ModelAdapter|None):

    if 'usage' not in response_from_llm or response_from_llm['usage'] is None:

        logger.debug(f'compute_usage_from_dict response_from_llm = {response_from_llm}')
        
        content: str = generate_prompt_text_from_messages([response_from_llm['choices'][0]['message']])
        prompt_tokens = count_tokens_from_messages(messages, model)
        completion_tokens = count_tokens_from_text(content, model)
        usage = {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens
        }

    else:

        logger.debug(f'compute_usage_from_dict with usage coming from LLM response = {response_from_llm["usage"]}')
        usage = response_from_llm.get('usage')

    return usage

def compute_usage_from_text(messages: dict, response_from_llm: str, model: ModelAdapter|None) -> CompletionUsage:

    logger.debug(f'compute_usage_from_text response_from_llm = {response_from_llm}')

    prompt_tokens = count_tokens_from_messages(messages, model)
    completion_tokens = count_tokens_from_text(response_from_llm, model)
    usage: CompletionUsage = CompletionUsage({
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens
    })
    return usage


def wrap_chat_completion_response(  # pylint: disable=too-many-arguments
    request_id: str,
    model: str,
    output_texts: List[str],
    finish_reasons: List[str],
    tool_calls_list: Optional[List[List[ChatToolCall]]] = None,
    logprob_results: Optional[List[List[LogProbsContent]]] = None,
    use_function_calling: Optional[bool] = None,
    usage: Optional[CompletionUsage] = None,
) -> ChatCompletionResponse:
    """Wrap the non-streaming chat completion results to ChatCompletionResponse instance."""
    return ChatCompletionResponse(
        id=request_id,
        choices=[
            ChatCompletionResponseChoice(
                index=i,
                finish_reason=finish_reasons[i],
                message=(
                    ChatCompletionMessage(role="assistant", content=output_text)
                ),
                logprobs=(
                    LogProbs(content=logprob_results[i])
                    if logprob_results is not None
                    else None
                ),
            )
            for i, (output_text, finish_reason) in enumerate(
                zip(output_texts, finish_reasons)
            )
        ],
        model=model,
        system_fingerprint="",
        usage=usage
    )

def wrap_completion_response(  # pylint: disable=too-many-arguments
    request_id: str,
    model: str,
    output_texts: List[str],
    finish_reasons: List[str],
    logprob_results: Optional[List[Optional[CompletionLogProbs]]] = None,
    usage: Optional[CompletionUsage] = None,
) -> CompletionResponse:
    """Wrap the non-streaming completion results to CompletionResponse instance."""
    return CompletionResponse(
        id=request_id,
        choices=[
            CompletionResponseChoice(
                index=i,
                finish_reason=finish_reason,
                text=output_text,
                logprobs=(
                    LogProbs(content=logprob_results[i])
                    if logprob_results is not None
                    else None
                )
            )
            for i, (output_text, finish_reason) in enumerate(zip(output_texts, finish_reasons))
        ],
        model=model,
        usage=usage,
    )