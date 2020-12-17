import json
from typing import Iterable

from cato import logger
from cato_server.domain.event import Event


def format_sse(events: Iterable[Event]) -> str:
    for e in events:
        message = f"event:{e.event_name}\ndata:{json.dumps(e.value)}\n\n"
        logger.info("Sending SSE %s", message)
        yield message
