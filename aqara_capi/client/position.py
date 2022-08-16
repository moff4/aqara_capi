from typing import Optional, Union

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

from aqara_capi.response import CloudApiResponse

from .base import BaseCloudApiClient


class ConfigPositionCreateModel(BaseModel):
    position_id: str = Field(alias='positionId')  # Position id


class PositionInfoModel(BaseModel):
    parent_position_id: Optional[str] = Field(alias='parentPositionId')  # Parent position id
    position_id: str = Field(alias='positionId')  # Position id
    position_name: Optional[str] = Field(alias='positionName')  # Position Name
    description: Optional[str] = Field(alias='description')  # Position Description
    create_time: int = Field(alias='createTime')  # Create time


class QueryPositionInfoModel(BaseModel):
    data: list[PositionInfoModel]
    total_count: int = Field(alias='totalCount')


class PositionCloudApiClient(BaseCloudApiClient):

    def config_position_create(
        self,
        name: str,
        description: Union[None, int, str] = None,  # according to doc type is int, that's unlogical :/
        parent_position_id: Union[None, int, str] = None,  # according to doc type is int, that's unlogical :/
    ) -> CloudApiResponse[ConfigPositionCreateModel]:
        data = {
            'positionName': name,
        }  # type: dict[str, Union[str, int]]
        if description is not None:
            data['description'] = description
        if parent_position_id is not None:
            data['parentPositionId'] = parent_position_id
        return self._request(
            intent='config.position.create',
            data=data,
            model=ConfigPositionCreateModel,
        )

    def config_position_update(
        self,
        position_id: str,
        name: str,
        description: Optional[str] = None,
    ) -> CloudApiResponse[None]:
        data = {
            'positionId': position_id,
            'positionName': name,
        }
        if description is not None:
            data['description'] = description
        return self._request(
            intent='config.position.update',
            data=data,
        )

    def config_position_delete(self, position_id: str) -> CloudApiResponse[None]:
        return self._request(
            intent='config.position.delete',
            data={
                'positionId': position_id,
            },
        )

    def query_position_info(
        self,
        # Parent position ID. When empty, query all positions under the user/project.
        parent_position_id: Optional[str] = None,
        page_num: int = 1,  # Page number, default value is 1. The minimum value is 1.
        page_size: int = 30,  # Number of items per page, default value is 30
    ) -> CloudApiResponse[QueryPositionInfoModel]:
        data = {
            'pageNum': page_num,
            'pageSize': page_size,
        }  # type: dict[str, Union[str, int]]
        if parent_position_id is not None:
            data['parentPositionId'] = parent_position_id

        return self._request(
            intent='query.position.info',
            data=data,
            model=QueryPositionInfoModel,
        )

    def query_position_detail(self, position_ids: list[str]) -> CloudApiResponse[list[PositionInfoModel]]:
        return self._request(
            intent='query.position.detail',
            data={
                'positionIds': position_ids,
            },
            model=PositionInfoModel,
            model_as_list=True
        )

    def config_position_timezone(
        self,
        position_id: str,
        timezone: str,  # like: 'GMT+08:00'
    ) -> CloudApiResponse[None]:
        return self._request(
            intent='config.position.timezone',
            data={
                'positionId': position_id,
                'timeZone': timezone,
            },
        )
