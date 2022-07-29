
# Aqara Cloud API

### Python SDK for Aqara Cloud API

_(Functionality is not full, but already has core for futher upgrades)_

### Example of usage

```python

from aqara_capi import CloudApiClient, Locality

# create client
client = CloudApiClient(
    app_id=APP_ID,  # your params from https://developer.aqara.com/console
    app_key=APP_KEY,
    key_id=KEY_ID,
    locality=Locality.RU,  # for cloud domain
)

# set access and refresh tokens
client.set_tokens(access_token='...', refresh_token='...')

# or generate them
client.get_auth_code(
    account='my@example.com',
    account_type=0,
    access_token_validity='7d',
)
client.get_access_token(
    auth_code='secret code from ur email',
    account='my@example.com',
    account_type=0,
)


# print your devices
response = client.query_device_info()
print(response.result)

# print device attributes
response = client.query_resource_info(
    model='lumi.light....',
)
print(response.result)

# trigger some action (for example turn on light)
client.write_resource_device(
    subject_id='lumi...',
    resource_id='4.1.85',
    value='1',
)

```