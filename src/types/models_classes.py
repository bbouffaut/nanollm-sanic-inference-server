from src.ports.model_port_echo import EchoModel
from src.ports.model_port_echo_with_tokenizer import EchoModelWithTokenizer
from src.ports.model_port_llama_cpp import LlamaCppModel
from src.ports.model_port_mock import MockModel
from src.ports.model_port_transformers import TransformersModel


class ModelClasses:
    LlamaCppModel = LlamaCppModel
    EchoModelWithTokenizer = EchoModelWithTokenizer
    EchoModel = EchoModel
    MockModel = MockModel
    TransformersModel = TransformersModel

    def get(self, name, default=None):
        return getattr(self, name, default)
    
MODEL_CLASSES = ModelClasses()

class ModelTypes:
    CHAT_COMPLETION = 'CHAT_COMPLETION'
    EMBEDDINGS = 'EMBEDDINGS'

MODEL_TYPES = ModelTypes()