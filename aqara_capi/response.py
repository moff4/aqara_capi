import logging
from typing import Any, Generic, Optional, Type, TypeVar

# pylint: disable=no-name-in-module
from pydantic import BaseModel, Field

# pylint: enable=no-name-in-module
from aqara_capi.consts import ErrorCode

logger = logging.getLogger(__name__)

SubModel = TypeVar('SubModel')


class CloudApiResponse(BaseModel, Generic[SubModel]):
    code: ErrorCode
    message: str
    request_id: str = Field(alias='requestId')
    msg_details: Optional[str] = Field(None, alias='msgDetails')
    result: Any

    data: SubModel = None  # type: ignore[assignment]

    def apply_data_model(self, model: Type[SubModel], as_list: bool = False) -> None:
        try:
            if as_list:
                self.data = [  # type: ignore[assignment]
                    model(**item)
                    for item in self.result
                ]
            else:
                self.data = model(**self.result)
        except Exception:
            logger.exception('model mapping failed')
