from dataclasses import dataclass
from typing import Any, Dict
import json  # Import json module to handle JSON data

@dataclass
class ModelInfo:
    name: str
    params: Dict[str, Any]

def from_json(json_input: Dict[str, Any]) -> ModelInfo:
    """Maps a JSON input to a ModelInfo instance."""
    return ModelInfo(
        name=json_input['name'],
        params=json_input['params']
    )