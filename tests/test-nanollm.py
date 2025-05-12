import argparse
import termcolor

from nano_llm import NanoLLM, ChatHistory

# parse arguments
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--model', type=str, default='google/gemma-2b-it', help="path to the model, or HuggingFace model repo")
parser.add_argument('--max-new-tokens', type=int, default=256, help="the maximum response length for each bot reply")
args = parser.parse_args()

# load model
model = NanoLLM.from_pretrained(
    model=args.model, 
    api='hf'
)

# create the chat history
chat_history = ChatHistory(model, system_prompt="You are a helpful and friendly AI assistant.")

while True:
    # enter the user query from terminal
    print('>> ', end='', flush=True)
    prompt = input().strip()

    # add user prompt and generate chat tokens/embeddings
    chat_history.append('user', prompt)
    embedding, position = chat_history.embed_chat()

    # generate bot reply
    reply = model.generate(
        embedding, 
        streaming=False, 
        kv_cache=chat_history.kv_cache,
        stop_tokens=chat_history.template.stop,
        max_new_tokens=args.max_new_tokens,
    )
        
    # stream the output
    #for token in reply:
    #    termcolor.cprint(token, 'blue', end='\n\n' if reply.eos else '', flush=True)
    print(reply)

    # save the final output
    chat_history.append('bot', reply)