from typing import Any, Union

# pylint: disable=no-name-in-module
from pydantic import BaseModel

# pylint: enable=no-name-in-module


class CloudApiResponse(BaseModel):
    code: int
    message: str
    msgDetails: str
    requestId: str
    result: Union[dict[str, Any], list[Any], None]
