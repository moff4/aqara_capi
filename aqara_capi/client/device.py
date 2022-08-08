from typing import Optional

from aqara_capi.types import CloudApiResponse

from .base import BaseCloudApiClient


class DeviceCloudApiClient(BaseCloudApiClient):

    def query_device_info(
        self,
        dids: Optional[list[str]] = None,
        position_id: Optional[str] = None,
        page_num: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> CloudApiResponse:
        return self._request(
            intent='query.device.info',
            data={
                'dids': dids,
                'positionId': position_id,
                'pageNum': page_num,
                'pageSize': page_size,
            },
        )

    def query_device_sub_info(self, did: str) -> CloudApiResponse:
        return self._request(
            intent='query.device.subInfo',
            data={'did': did},
        )
