from dataclasses import dataclass

from typing import List, Dict, Union


@dataclass
class Response:
    status_code: int


@dataclass
class JsonResponse:
    status_code: int
    content: Union[Dict, List]
