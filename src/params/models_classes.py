from ports.model_port_echo import EchoModel
from ports.model_port_echo_with_tokenizer import EchoModelWithTokenizer
from ports.model_port_llama_cpp import LlamaCppModel
from ports.model_port_mock import MockModel


MODEL_CLASSES = {
    'LlamaCppModel': LlamaCppModel,
    'EchoModelWithTokenizer': EchoModelWithTokenizer,
    'EchoModel': EchoModel,
    'MockModel': MockModel
    
}