from src.ports.model_port_echo import EchoModel
from src.ports.model_port_echo_with_tokenizer import EchoModelWithTokenizer
from src.ports.model_port_llama_cpp import LlamaCppModel
from src.ports.model_port_mock import MockModel


MODEL_CLASSES = {
    'LlamaCppModel': LlamaCppModel,
    'EchoModelWithTokenizer': EchoModelWithTokenizer,
    'EchoModel': EchoModel,
    'MockModel': MockModel
    
}

MODEL_TYPES = {
    'CHAT_COMPLETION': 'CHAT_COMPLETION',
    'EMBEDDINGS': 'EMBEDDINGS'
}