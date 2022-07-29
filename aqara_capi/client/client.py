
from .auth import AuthCloudApiClient
from .device import DeviceCloudApiClient
from .resource import ResourceCloudApiClient


class CloudApiClient(AuthCloudApiClient, DeviceCloudApiClient, ResourceCloudApiClient):
    ...
