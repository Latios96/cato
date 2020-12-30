import datetime
from typing import Optional

from dateutil.parser import parse

from cato_server.mappers.abstract_value_mapper import AbstractValueMapper


class DateTimeValueMapper(AbstractValueMapper[datetime.datetime, str]):
    def map_from(self, data: Optional[str]) -> Optional[datetime.datetime]:
        if data:
            return parse(data)

    def map_to(self, date: datetime.datetime) -> str:
        return date.isoformat()
