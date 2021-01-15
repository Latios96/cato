from cato_server.api.utils import format_sse
from cato_server.domain.event import Event


def test_format_sse():
    sse_events = list(
        format_sse([Event("EVENT_NAME", "VALUE1"), Event("EVENT_NAME", "VALUE2")])
    )

    assert sse_events == [
        'event:EVENT_NAME\ndata:"VALUE1"\n\n',
        'event:EVENT_NAME\ndata:"VALUE2"\n\n',
    ]
