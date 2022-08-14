from typing import Any, Optional, Type

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

from aqara_capi.consts import ErrorCode
from aqara_capi.response import CloudApiResponse, SubModel

from .base import BaseCloudApiClient


class GetAuthModel(BaseModel):
    auth_code: str = Field(alias='authCode')


class AccessTokenModel(BaseModel):
    expires_in: str = Field(alias='expiresIn')
    open_id: str = Field(alias='openId')
    access_token: str = Field(alias='accessToken')
    refresh_token: str = Field(alias='refreshToken')


class AuthCloudApiClient(BaseCloudApiClient):

    def _request(
        self,
        intent: str,
        data: Any,
        model: Optional[Type[BaseModel]] = None,
        model_as_list: bool = False,
    ) -> CloudApiResponse[SubModel]:
        res = self._raw_request(
            intent=intent,
            data=data,
            model=model,
            model_as_list=model_as_list,
        )  # type: CloudApiResponse[SubModel]
        if res.code == ErrorCode.CODE_108:
            self.logger.warning('need to refresh access token')
            self.refresh_access_token()
            res = self._raw_request(intent=intent, data=data, model=model, model_as_list=model_as_list)
        elif res.code != ErrorCode.CODE_SUCCESS:
            self.logger.error('unexpected code "%s" for intent "%s"', res.code, intent)
        return res

    def get_auth_code(
        self,
        account: str,
        account_type: int,
        access_token_validity: str = '7d',
    ) -> CloudApiResponse[GetAuthModel]:
        return self._request(
            intent='config.auth.getAuthCode',
            data={
                'account': account,
                'accountType': account_type,
                'accessTokenValidity': access_token_validity,
            },
            model=GetAuthModel
        )

    def get_access_token(self, auth_code: str, account: str, account_type: int) -> CloudApiResponse[AccessTokenModel]:
        res = self._request(
            intent='config.auth.getToken',
            data={
                'authCode': auth_code,
                'account': account,
                'accountType': account_type,
            },
            model=AccessTokenModel,
        )  # type: CloudApiResponse[AccessTokenModel]
        if res.code == ErrorCode.CODE_SUCCESS:
            result = res.result  # type: AccessTokenModel
            self.set_tokens(access_token=result.access_token, refresh_token=result.refresh_token)
        return res

    def refresh_access_token(self) -> CloudApiResponse[AccessTokenModel]:
        res = self._request(
            intent='config.auth.refreshToken',
            data={
                'refreshToken': self._refresh_token,
            },
            model=AccessTokenModel,
        )  # type: CloudApiResponse[AccessTokenModel]
        if res.code == ErrorCode.CODE_SUCCESS:
            result = res.result  # type: AccessTokenModel
            self.set_tokens(access_token=result.access_token, refresh_token=result.refresh_token)
        return res
