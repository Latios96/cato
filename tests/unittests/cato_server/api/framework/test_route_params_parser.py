import pytest

from cato_server.api.framework.abstract.route_params_parser import (
    RouteParamsParser,
    RouteParam,
    RouteParamType,
)


@pytest.mark.parametrize(
    "route,expected",
    [
        ("/test", []),
        ("/test/<id>", [RouteParam(type=RouteParamType.STRING, name="id")]),
        (
            "/test/<id>/<otherId>",
            [
                RouteParam(type=RouteParamType.STRING, name="id"),
                RouteParam(type=RouteParamType.STRING, name="otherId"),
            ],
        ),
        (
            "/test/<int:id>/<uuid:uuid>",
            [
                RouteParam(type=RouteParamType.INTEGER, name="id"),
                RouteParam(type=RouteParamType.UUID, name="uuid"),
            ],
        ),
        (
            "/test/<int>/<uuid:uuid>/foo/bar/<int:foozableId>/<string:test>",
            [
                RouteParam(type=RouteParamType.STRING, name="int"),
                RouteParam(type=RouteParamType.UUID, name="uuid"),
                RouteParam(type=RouteParamType.INTEGER, name="foozableId"),
                RouteParam(type=RouteParamType.STRING, name="test"),
            ],
        ),
    ],
)
def test_parse_success(route, expected):
    parser = RouteParamsParser()

    result = parser.parse_route(route)

    assert result == expected
