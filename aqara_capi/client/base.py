import time
from hashlib import md5
from logging import getLogger
from typing import Any, Optional
from urllib.parse import urlencode

import requests

from aqara_capi.consts import API_DOMAIN, Locality
from aqara_capi.misc import get_random_string
from aqara_capi.types import CloudApiResponse


class BaseCloudApiClient:
    __slots__ = (
        'app_id',
        'app_key',
        'key_id',
        'locality',
        '_access_token',
        '_refresh_token',
        '_api_url',
        '_request_props',
    )

    logger = getLogger(__name__)

    def __init__(
        self,
        app_id: str,
        app_key: str,
        key_id: str,
        locality: Locality,
        request_props: Optional[dict[str, Any]] = None,
    ) -> None:
        self.app_id = app_id
        self.app_key = app_key
        self.key_id = key_id

        self._access_token = ''
        self._refresh_token = ''

        self._api_url = f"https://{API_DOMAIN[locality]}/v3.0/open/api"
        self._request_props = request_props or {}  # type: dict[str, Any]

    def _get_request_headers(self) -> dict[str, str]:
        nonce = get_random_string(5)
        timestamp = str(int(time.time() * 1000))

        headers = {
            'Keyid': self.key_id,
            'Appid': self.app_id,
            'Nonce': nonce,
            'Time': timestamp,
        }  # type: dict[str, str]

        if self._access_token:
            headers['Accesstoken'] = self._access_token

        seed = (urlencode([(key, headers[key]) for key in sorted(headers)]) + self.app_key).lower()
        return headers | {'sign': md5(seed.encode('utf-8')).hexdigest()}

    def _raw_request(
        self,
        intent: str,
        data: Any,
    ) -> CloudApiResponse:

        headers = self._get_request_headers()
        payload = {'intent': intent, 'data': data}

        resp = requests.post(
            url=self._api_url,
            json=payload,
            headers=headers,
            **self._request_props,
        )
        self.logger.debug('request[%s] got status: %s', intent, resp.status_code)

        resp.raise_for_status()
        return CloudApiResponse(**resp.json())

    def _request(
        self,
        intent: str,
        data: Any,
    ) -> CloudApiResponse:
        res = self._raw_request(intent=intent, data=data)
        if res.code != 0:
            self.logger.error('unexpected code "%s" for intent "%s"', res.code, intent)
        return res

    def set_tokens(self, access_token: str, refresh_token: str) -> None:
        self._access_token = access_token
        self._refresh_token = refresh_token
