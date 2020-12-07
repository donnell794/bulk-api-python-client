import pytest

from unittest import mock
from unittest.mock import call

from bulk_api_client import client


def test_models():
    FakeClient = mock.MagicMock()
    FakeClient.definitions = {
        "app1.model_one": {},
        "app1.model_two": {},
        "app2.model_three": {},
    }
    FakeApp1 = mock.MagicMock()
    FakeApp2 = mock.MagicMock()
    FakeClient.return_value.app.side_effects = [
        FakeApp1,
        FakeApp2,
    ]
    FakeModel1 = "model1"
    FakeModel2 = "model2"
    FakeApp1.return_value.model.side_effects = [
        FakeModel1,
        FakeModel2,
    ]
    FakeModel3 = "model3"
    FakeApp2.return_value.model.side_effects = [
        FakeModel3,
    ]
    with pytest.setenv(BULK_API_TOKEN="token"):
        with mock.patch.object(client, "Client", return_value=FakeClient):
            pytest.reimport_env_client()
            from bulk_api_client import models

            FakeClient.app.assert_has_calls(
                [call("app1"), call("app2"),]
            )
