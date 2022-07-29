from aqara_capi.types import CloudApiResponse

from .base import BaseCloudApiClient


class ResourceCloudApiClient(BaseCloudApiClient):

    def query_resource_info(self, model: str, resource_id: str | None = None) -> CloudApiResponse:
        return self._request(
            intent='query.resource.info',
            data={
                'model': model,
                'resourceId': resource_id,
            }
        )

    def query_resource_value(self, subject_id: str, resource_ids: list[str]) -> CloudApiResponse:
        return self._request(
            intent='query.resource.value',
            data={'resources': [{'subjectId': subject_id, 'resourceIds': resource_ids}]},
        )

    def write_resource_device(self, subject_id: str, resource_id: str, value: str) -> CloudApiResponse:
        return self._request(
            intent='write.resource.device',
            data={
                'list_data': True,
                'subjectId': subject_id,
                'resources': [
                    {'resourceId': resource_id, 'value': value}
                ]
            },
        )
