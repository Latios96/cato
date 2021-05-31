import re
from dataclasses import dataclass
from enum import Enum

from typing import List

PARAM_PATTERN = re.compile("<((int|string|uuid):)?(\w+)>")


class RouteParamType(Enum):
    STRING = "string"
    INTEGER = "int"
    UUID = "uuid"


@dataclass
class RouteParam:
    type: RouteParamType
    name: str


class RouteParamsParser:
    def parse_route(self, route: str) -> List[RouteParam]:
        results = []
        finditer = re.finditer(PARAM_PATTERN, route)
        for r in finditer:
            _, type, name = r.groups()
            if not type:
                type = "string"
            results.append(RouteParam(type=RouteParamType(type), name=name))
        return results

    def to_fast_api(self, route: str):
        return re.sub(PARAM_PATTERN, r"{\g<3>}", route)
