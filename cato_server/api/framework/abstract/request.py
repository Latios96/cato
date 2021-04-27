from typing import Dict


class AbstractRequest:
    def json(self) -> Dict:
        raise NotImplementedError()
