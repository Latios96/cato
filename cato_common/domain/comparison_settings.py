from dataclasses import dataclass

from cato_common.domain.comparison_method import ComparisonMethod


@dataclass
class ComparisonSettings:
    method: ComparisonMethod
    threshold: float

    @staticmethod
    def default():
        return ComparisonSettings(method=ComparisonMethod.SSIM, threshold=0.8)
