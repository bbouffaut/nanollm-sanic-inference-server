from dataclasses import dataclass
from typing import Any, Dict, Literal

@dataclass
class ModelInfo:
    name: str
    params: Dict[str, Any]
    type: Literal['CHAT_COMPLETION', 'EMBEDDINGS']

def from_json(json_input: Dict[str, Any]) -> ModelInfo:
    """Maps a JSON input to a ModelInfo instance."""
    return ModelInfo(
        name=json_input['name'],
        params=json_input['params']
    )