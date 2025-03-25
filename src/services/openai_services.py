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

def compute_usage_from_text(messages: dict, response_from_llm: str, model: ModelAdapter|None):

    logger.debug(f'compute_usage_from_text response_from_llm = {response_from_llm}')

    prompt_tokens = count_tokens_from_messages(messages, model)
    completion_tokens = count_tokens_from_text(response_from_llm, model)
    usage = {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens
    }
    return usage