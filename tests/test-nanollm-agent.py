from nano_llm import NanoLLM, ChatHistory, BotFunctions, bot_function
from datetime import datetime

@bot_function
def DATE():
    """ Returns the current date. """
    return datetime.now().strftime("%A, %B %-m %Y")
   
@bot_function
def TIME():
    """ Returns the current time. """
    return datetime.now().strftime("%-I:%M %p")
          
# load the model   
model = NanoLLM.from_pretrained(
    model="meta-llama/Meta-Llama-3-8B-Instruct", 
    api='hf'
)

# create the chat history
system_prompt = "You are a helpful and friendly AI assistant." + BotFunctions.generate_docs()
chat_history = ChatHistory(model, system_prompt=system_prompt)

while True:
    # enter the user query from terminal
    print('>> ', end='', flush=True)
    prompt = input().strip()

    # add user prompt and generate chat tokens/embeddings
    chat_history.append(role='user', msg=prompt)
    embedding, position = chat_history.embed_chat()

    # generate bot reply (give it function access)
    reply = model.generate(
        embedding, 
        streaming=True, 
        functions=BotFunctions(),
        kv_cache=chat_history.kv_cache,
        stop_tokens=chat_history.template.stop
    )
        
    # stream the output
    for token in reply:
        print(token, end='\n\n' if reply.eos else '', flush=True)

    # save the final output
    chat_history.append(role='bot', text=reply.text, tokens=reply.tokens)
    chat_history.kv_cache = reply.kv_cache