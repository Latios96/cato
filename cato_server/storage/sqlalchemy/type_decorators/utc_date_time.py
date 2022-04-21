import datetime

from sqlalchemy.types import DateTime, TypeDecorator


class UtcDateTime(TypeDecorator):

    impl = DateTime(timezone=False)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return
        if not isinstance(value, datetime.datetime):
            raise TypeError("expected datetime.datetime, not " + repr(value))
        if self._is_naive_datetime_object(value):
            raise ValueError("Naive datetime objects are not allowed")
        return value.astimezone(datetime.timezone.utc).replace(tzinfo=None)

    def _is_naive_datetime_object(self, value):
        none = value.tzinfo is None
        return none

    def process_result_value(self, value, dialect):
        if value is None:
            return
        if not self._is_naive_datetime_object(value):
            raise ValueError("Expected naive datetime object")
        return value.replace(tzinfo=datetime.timezone.utc)
