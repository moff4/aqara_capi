
from aqara_capi.consts import ErrorCode

from .auth import AuthCloudApiClient
from .device import DeviceCloudApiClient, DeviceInfoModel
from .resource import ResourceCloudApiClient


class CloudApiClient(AuthCloudApiClient, DeviceCloudApiClient, ResourceCloudApiClient):

    def get_all_devices(self) -> list[DeviceInfoModel]:
        devices = []  # type: list[DeviceInfoModel]
        total_count = 42
        page_size = 100
        page_num = 0

        while len(devices) < total_count:
            resp = self.query_device_info(page_num=page_num, page_size=page_size)
            if resp.code != ErrorCode.CODE_SUCCESS:
                raise ValueError('api request failed')

            total_count = resp.data.total_count
            devices.extend(resp.data.data)
            page_num += 1

        return devices
