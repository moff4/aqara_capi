from typing import Optional

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

from aqara_capi.response import CloudApiResponse

from .base import BaseCloudApiClient


class DeviceInfoModel(BaseModel):
    did: str
    device_name: Optional[str] = Field(None, alias='deviceName')
    parent_did: Optional[str] = Field(None, alias='parentDid')
    position_id: str = Field(alias='positionId')
    timezone: str = Field(alias='timeZone')
    model: str
    model_type: int = Field(alias='modelType')
    state: int
    firmware_version: Optional[str] = Field(None, alias='firmwareVersion')
    create_time: int = Field(alias='createTime')
    update_time: int = Field(alias='updateTime')


class QueryDeviceInfoModel(BaseModel):
    data: list[DeviceInfoModel]
    total_count: int


class DeviceCloudApiClient(BaseCloudApiClient):

    def query_device_info(
        self,
        dids: Optional[list[str]] = None,
        position_id: Optional[str] = None,
        page_num: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> CloudApiResponse[QueryDeviceInfoModel]:
        return self._request(
            intent='query.device.info',
            data={
                'dids': dids,
                'positionId': position_id,
                'pageNum': page_num,
                'pageSize': page_size,
            },
            model=QueryDeviceInfoModel,
        )

    def query_device_sub_info(self, did: str) -> CloudApiResponse[list[DeviceInfoModel]]:
        return self._request(
            intent='query.device.subInfo',
            data={'did': did},
            model=DeviceInfoModel,
            model_as_list=True,
        )
