from copy import deepcopy

from bulk_api_client.exceptions import InvalidQObject


class Q:
    OPERATORS = ["AND", "OR"]

    def __init__(self, **kwargs):
        if not len(kwargs.keys()) == 1:
            raise NotImplementedError

        key, value = list(kwargs.items())[0]
        if not isinstance(key, str):
            raise TypeError
        elif key in self.OPERATORS:
            if isinstance(value, list):

                if not all([isinstance(v, Q) for v in value]):
                    raise InvalidQObject(
                        "Values for {} must be list of Q objects".format(key)
                    )
            elif isinstance(value, dict):
                pass
        self._filter = deepcopy(kwargs)

    def _combine(self, object_on_right, conn):
        return Q(**{conn: [self._filter, object_on_right.output_filter()]})

    def __and__(self, object_on_right):

        return self._combine(object_on_right, self.OPERATORS[0])

    def __or__(self, object_on_right):
        return self._combine(object_on_right, self.OPERATORS[1])

    def output_filter(self):
        return self._filter
