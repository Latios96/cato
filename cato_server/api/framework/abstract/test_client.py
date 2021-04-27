from typing import Dict


class AbstractResponse:
    @property
    def json(self) -> Dict:
        raise NotImplementedError()

    @property
    def status_code(self) -> int:
        raise NotImplementedError()


class AbstractTestClient:
    def get(self, url: str) -> AbstractResponse:
        raise NotImplementedError()

    def post(self, url: str) -> AbstractResponse:
        raise NotImplementedError()
