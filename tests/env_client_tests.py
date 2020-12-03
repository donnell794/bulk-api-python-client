import os
import imp
import pytest

from unittest import mock

from bulk_api_client.exceptions import BulkAPIError
from bulk_api_client.client import Client


def reimport_env_client():
    from bulk_api_client import env_client

    imp.reload(env_client)
    return env_client.env_client


def test_env_client_missing_token():
    os.environ["BULK_API_TOKEN"] = ""
    with pytest.raises(BulkAPIError) as msg:
        reimport_env_client()

    assert (
        str(msg.value) == "Environment variable BULK_API_TOKEN was not found."
    )


def test_env_client():
    token = "token"
    os.environ["BULK_API_TOKEN"] = token
    url = "url"
    os.environ["BULK_API_URL"] = url
    expiration_time = "100"
    os.environ["BULK_API_EXPIRATION_TIME"] = expiration_time
    with mock.patch.object(Client, "__init__", return_value=None) as fn:
        env_client = reimport_env_client()
    fn.assert_called_with(
        token, api_url=url, expiration_time=int(expiration_time)
    )
    assert isinstance(env_client, Client)
