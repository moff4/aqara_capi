from aqara_capi.types import CloudApiResponse

from .base import BaseCloudApiClient


class DeviceCloudApiClient(BaseCloudApiClient):

    def query_device_info(
        self,
        dids: list[str] | None = None,
        position_id: str | None = None,
        page_num: int | None = None,
        page_size: int | None = None,
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
