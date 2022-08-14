from typing import Any, Optional

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

from aqara_capi.response import CloudApiResponse

from .base import BaseCloudApiClient


class QueryResourceInfoModel(BaseModel):
    enums: Optional[str] = None  # Enums description
    resource_id: str = Field(alias='resourceId')  # Resource id
    min_value: Optional[int] = Field(None, alias='minValue')  # Minimum value
    unit: int  # Unit
    access: int  # 0-read 1-write 2-write/read
    max_value: Optional[int] = Field(None, alias='maxValue')  # Maxinum value
    default_value: Optional[str] = Field(None, alias='defaultValue')  # Default value
    name: str  # Name
    description: str  # Description
    model: str  # Subject model


class QueryResourceValueModel(BaseModel):
    subject_id: str = Field(alias='subjectId')  # Device id
    resource_id: str = Field(alias='resourceId')  # Resource id
    value: str = Field(alias='value')  # Resource value
    timestamp: int = Field(alias='timeStamp')  # Time stamp(the unit is ms)


class ResourceCloudApiClient(BaseCloudApiClient):

    def query_resource_info(
        self,
        model: str,
        resource_id: Optional[str] = None,
    ) -> CloudApiResponse[QueryResourceInfoModel]:
        return self._request(
            intent='query.resource.info',
            data={
                'model': model,
                'resourceId': resource_id,
            },
            model=QueryResourceInfoModel,
        )

    def query_resource_value(
        self,
        subject_id: str,
        resource_ids: list[str],
    ) -> CloudApiResponse[list[QueryResourceValueModel]]:
        return self._request(
            intent='query.resource.value',
            data={'resources': [{'subjectId': subject_id, 'resourceIds': resource_ids}]},
            model=QueryResourceValueModel,
            model_as_list=True,
        )

    def multi_query_resource_value(
        self,
        subject_resource_mapping: dict[str, list[str]],
    ) -> CloudApiResponse[list[QueryResourceValueModel]]:
        """
            same as cls.query_resource_value() but for several subject ids at once
            subject_resource_mapping - {subject_id => list[resource_id]}
        """
        return self._request(
            intent='query.resource.value',
            data={
                'resources': [
                    {'subjectId': sid, 'resourceIds': rids}
                    for sid, rids in subject_resource_mapping.items()
                ]
            },
            model=QueryResourceValueModel,
            model_as_list=True,
        )

    def write_resource_device(self, subject_id: str, resource_id: str, value: str) -> CloudApiResponse[Any]:
        return self._request(
            intent='write.resource.device',
            data=[
                {
                    'subjectId': subject_id,
                    'resources': [
                        {'resourceId': resource_id, 'value': value}
                    ]
                },
            ],
        )
