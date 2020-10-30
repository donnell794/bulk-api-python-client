import pytest

from bulk_api_client.query_helpers import Q
from bulk_api_client.exceptions import InvalidQObject


def test_init_q_obj():
    q_obj = Q(test_field="test")
    assert q_obj.output_filter() == {"test_field": "test"}


def test_q_obj_chain():
    q_obj_chain = Q(test_field="test1") & Q(test_field="test2")

    assert q_obj_chain.output_filter() == {
        "AND": [{"test_field": "test1"}, {"test_field": "test2"}]
    }


@pytest.mark.parametrize(
    "q_dict,error",
    [
        ({"test_field": "test", "fail_field": "fail"}, NotImplementedError),
        ({"test_field": ["invalid"]}, InvalidQObject),
        ({1: 1}, TypeError),
        ({None: 1}, TypeError),
        (
            {"test": {"test_field": "test", "fail_field": "fail"}},
            InvalidQObject,
        ),
    ],
)
def test_init_q_obj_failure(q_dict, error):
    with pytest.raises(error):
        Q(**q_dict)
