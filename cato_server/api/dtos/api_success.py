from dataclasses import dataclass


@dataclass
class ApiSuccess:  # todo this belogns to cato_common
    success: bool

    @staticmethod
    def ok():
        # type: ()->ApiSuccess
        return ApiSuccess(True)
