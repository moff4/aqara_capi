from typing import Any, Optional

# pylint: disable=no-name-in-module
from pydantic import BaseModel, Field

# pylint: enable=no-name-in-module


class CloudApiResponse(BaseModel):
    code: int
    message: str
    request_id: str = Field(alias='requestId')
    msg_details: Optional[str] = Field(None, alias='msgDetails')
    result: Any
