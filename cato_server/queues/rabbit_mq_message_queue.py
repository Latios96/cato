import json

import pika
from typing import Iterable

from cato_server.domain.event import Event
from cato_server.mappers.abstract_class_mapper import AbstractClassMapper
from cato_server.queues.abstract_message_queue import AbstractMessageQueue, T

import logging

logger = logging.getLogger(__name__)


class RabbitMqMessageQueue(AbstractMessageQueue):
    def __init__(self, host):
        self._host = host

    def send_event(
        self,
        exchange_name: str,
        routing_key: str,
        event: Event[T],
        message_mapper: AbstractClassMapper[T],
    ):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._host))

        channel = connection.channel()

        channel.exchange_declare(exchange=exchange_name, exchange_type="direct")

        event_message = {
            "name": event.event_name,
            "value": message_mapper.map_to_dict(event.value),
        }
        message = json.dumps(event_message)
        channel.basic_publish(
            exchange=exchange_name, routing_key=routing_key, body=message
        )
        connection.close()

    def get_event_stream(
        self,
        exchange_name: str,
        routing_key: str,
        message_mapper: AbstractClassMapper[T],
    ) -> Iterable[Event[T]]:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._host))
        channel = connection.channel()

        channel.exchange_declare(exchange=exchange_name, exchange_type="direct")

        result = channel.queue_declare(queue="", exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(
            exchange=exchange_name, queue=queue_name, routing_key=routing_key
        )

        while True:
            message = channel.basic_get(queue=queue_name)
            if message != (None, None, None):
                method, properties, body = message
                event_dict = json.loads(body)
                event = Event(event_dict["name"], event_dict["value"])
                yield event
