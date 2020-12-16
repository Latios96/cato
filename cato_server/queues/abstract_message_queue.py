from typing import TypeVar, Iterable

from cato_server.domain.event import Event
from cato_server.mappers.abstract_class_mapper import AbstractClassMapper

T = TypeVar("T")


class AbstractMessageQueue:
    def send_event(
        self,
        exchange_name: str,
        routing_key: str,
        event: Event[T],
        value_mapper: AbstractClassMapper[T],
    ):
        raise NotImplementedError()

    def get_event_stream(
        self,
        exchange_name: str,
        routing_key: str,
        value_mapper: AbstractClassMapper[T],
    ) -> Iterable[Event[T]]:
        raise NotImplementedError()
