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
    FakeClient.app.side_effect = [
        FakeApp1,
        FakeApp2,
    ]
    FakeModel1 = "model1"
    FakeModel2 = "model2"
    FakeApp1.model.side_effect = [
        FakeModel1,
        FakeModel2,
    ]
    FakeModel3 = "model3"
    FakeApp2.model.side_effect = [
        FakeModel3,
    ]
    with pytest.setenv(BULK_API_TOKEN="token"):
        with mock.patch.object(client, "Client", return_value=FakeClient):
            pytest.reimport_env_client()
            from bulk_api_client import models

    FakeClient.app.assert_has_calls(
        [call("app1"), call("app2"),]
    )
    FakeApp1.model.assert_has_calls(
        [call("model_one"), call("model_two"),]
    )
    FakeApp2.model.assert_has_calls(
        [call("model_three"),]
    )
    assert all(
        [
            models.app1.ModelOne == FakeModel1,
            models.app1.ModelTwo == FakeModel2,
            models.app2.ModelThree == FakeModel3,
        ]
    )
