from dataclasses import dataclass


@dataclass(frozen=True)
class BranchName:
    name: str

    def __str__(self):
        return self.name

    def __post_init__(self):
        if not self.name:
            raise ValueError("Branch name can not be empty!")
