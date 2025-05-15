"""Error protocols in MLC LLM"""

from http import HTTPStatus
from typing import Optional

from pydantic import BaseModel


class BadRequestError(ValueError):
    """The exception for bad requests in engines."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ErrorResponse(BaseModel):
    """The class of error response."""

    object: str = "error"
    message: str
    code: Optional[int] = None
