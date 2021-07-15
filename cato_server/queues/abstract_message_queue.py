from typing import TypeVar, Iterable

from cato_server.domain.event import Event
from cato_server.mappers.object_mapper import ObjectMapper

T = TypeVar("T")


class AbstractMessageQueue:
    def send_event(
        self,
        exchange_name: str,
        routing_key: str,
        event: Event[T],
        object_mapper: ObjectMapper,
    ) -> None:
        raise NotImplementedError()

    def get_event_stream(
        self,
        exchange_name: str,
        routing_key: str,
        object_mapper: ObjectMapper,
    ) -> Iterable[Event[T]]:
        raise NotImplementedError()
