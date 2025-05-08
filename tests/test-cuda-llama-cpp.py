from llama_cpp import Llama
llm = Llama(model_path='/data/models/huggingface/gemma-2-2b-it-Q3_K_L.gguf', chat_format="chatml", n_gpu_layers=-1)


messages = [
    {
    "role": "system",
    "content": "Tu es un assistant capable de formuler une réponse à une questions qui te sera fournie à partir d'éléments de réponse fournis également. Tu dois utiliser uniquement les éléments de réponse fournis pour constuire ta réponse. Tu dois utiliser toutes les informations fournies. Le nom du massif doit être mentionné dans ta réponse."
    },
    {
    "role": "user",
    "content": "Voici la question: 'Quelle est la qualité de la neige en Vanoise?'. Voici les éléments de réponse à utiliser pour construire ta réponse: 'En dessous de 2000m, la neige est pourrie. au dessus, en face nord, on trouve de la neige de printemps. On peut encore trouver de la neige froide en face nors au delà de 3000m'"
    }
]

response = llm.create_chat_completion(
    messages=messages,
    temperature=0.7,
    stream=True
)
for chunk in response:
    # print(chunk['choices'][0]['text'].split('[/INST]')[-1])
    if 'content' in chunk['choices'][0]['delta']:
        print(chunk['choices'][0]['delta']['content'])

