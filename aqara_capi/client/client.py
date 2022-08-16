from typing import Any, Callable, TypeVar

from aqara_capi.consts import ErrorCode
from aqara_capi.response import CloudApiResponse

from .auth import AuthCloudApiClient
from .device import DeviceCloudApiClient, DeviceInfoModel
from .position import PositionCloudApiClient, PositionInfoModel
from .resource import ResourceCloudApiClient

Model = TypeVar('Model')


class CloudApiClient(
    AuthCloudApiClient,
    DeviceCloudApiClient,
    ResourceCloudApiClient,
    PositionCloudApiClient,
):

    @staticmethod
    def _page_iter(
        method: Callable[[int, int], CloudApiResponse[Any]],
        page_size: int,
    ) -> list[Any]:
        objs = []  # type: list[Any]
        total_count = 42
        page_num = 1

        while len(objs) < total_count:
            resp = method(page_num=page_num, page_size=page_size)  # type: ignore
            if resp.code != ErrorCode.CODE_SUCCESS:
                raise ValueError('api request failed')

            total_count = resp.data.total_count
            objs.extend(resp.data.data)
            page_num += 1

        return objs

    def get_all_devices(self, page_size: int = 100) -> list[DeviceInfoModel]:
        return self._page_iter(
            method=self.query_device_info,  # type: ignore
            page_size=page_size,
        )

    def get_all_positions(self, page_size: int = 100) -> list[PositionInfoModel]:
        return self._page_iter(
            method=self.query_position_info,  # type: ignore
            page_size=page_size,
        )
