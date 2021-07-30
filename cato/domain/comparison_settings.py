from dataclasses import dataclass

from cato.domain.comparison_method import ComparisonMethod


@dataclass
class ComparisonSettings:
    method: ComparisonMethod
    threshold: float
