from typing import Any, cast

from aqara_capi.types import CloudApiResponse

from .base import BaseCloudApiClient


class AuthCloudApiClient(BaseCloudApiClient):

    def _request(
        self,
        intent: str,
        data: Any,
    ) -> CloudApiResponse:
        res = self._raw_request(intent=intent, data=data)
        if res.code == 108:
            self.logger.warning('need to refresh access token')
            self.refresh_access_token()
            res = self._raw_request(intent=intent, data=data)
        elif res.code != 0:
            self.logger.error('unexpected code "%s" for intent "%s"', res.code, intent)
        return res

    def get_auth_code(
        self,
        account: str,
        account_type: int,
        access_token_validity: str = '7d',
    ) -> CloudApiResponse:
        return self._request(
            intent='config.auth.getAuthCode',
            data={
                'account': account,
                'accountType': account_type,
                'accessTokenValidity': access_token_validity,
            }
        )

    def get_access_token(self, auth_code: str, account: str, account_type: int) -> CloudApiResponse:
        res = self._request(
            intent='config.auth.getToken',
            data={
                'authCode': auth_code,
                'account': account,
                'accountType': account_type,
            }
        )
        if res.code == 0:
            result = cast(dict[str, str], res.result)
            self.set_tokens(access_token=result['accessToken'], refresh_token=result['refreshToken'])
        return res

    def refresh_access_token(self) -> CloudApiResponse:
        res = self._request(
            intent='config.auth.refreshToken',
            data={
                'refreshToken': self._refresh_token,
            },
        )
        if res.code == 0:
            result = cast(dict[str, str], res.result)
            self.set_tokens(access_token=result['accessToken'], refresh_token=result['refreshToken'])
        return res
