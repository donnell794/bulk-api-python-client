from bulk_api_client.exceptions import InvalidQObject


class Q:
    AND = "AND"
    OR = "OR"
    default = AND

    def __init__(self, _conn=None, **kwargs):
        self._conn = _conn or self.default
        self._children = list(kwargs.items())

    def _combine(self, object_on_right, conn):
        if not isinstance(object_on_right, Q):
            raise InvalidQObject(
                "{} must be a Q object".format(object_on_right)
            )

        if not object_on_right._children:
            return self

        elif not self._children:
            return object_on_right

        q = Q(_conn=conn)
        for operand in [self, object_on_right]:
            if (conn == operand._conn and operand._children) or len(
                operand._children
            ) == 1:
                q._children.extend(operand._children)
            else:
                q._children.append(operand)

        return q

    def __and__(self, object_on_right):
        return self._combine(object_on_right, self.AND)

    def __or__(self, object_on_right):
        return self._combine(object_on_right, self.OR)

    def __eq__(self, object_on_right):
        return (
            self.__class__ == other.__class__
            and self._conn == object_on_right._conn
            and self._children == object_on_right._children
        )

    def output_filter(self):
        return {
            self._conn: [
                c.output_filter() if isinstance(c, Q) else {c[0]: c[1]}
                for c in self._children
            ]
        }
