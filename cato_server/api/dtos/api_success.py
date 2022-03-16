from dataclasses import dataclass


@dataclass
class ApiSuccess:
    success: bool

    @staticmethod
    def ok():
        # type: ()->ApiSuccess
        return ApiSuccess(True)
