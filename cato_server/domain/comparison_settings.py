from dataclasses import dataclass

from cato_server.domain.comparison_method import ComparisonMethod


@dataclass
class ComparisonSettings:
    method: ComparisonMethod
    threshold: float
