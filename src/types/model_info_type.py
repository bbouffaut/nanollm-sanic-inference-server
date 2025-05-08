from dataclasses import dataclass
from typing import Any, Dict, Literal

@dataclass
class ModelParams:
    model_path: str
    gpu: bool

@dataclass
class ModelInfo:
    name: str
    params: ModelParams
    type: Literal['CHAT_COMPLETION', 'EMBEDDINGS', "NONE"]

def from_json(json_input: Dict[str, Any]) -> ModelInfo:
    """Maps a JSON input to a ModelInfo instance."""
    return ModelInfo(
        name=json_input['name'],
        params=json_input['params'],
        type=json_input['type']
    )