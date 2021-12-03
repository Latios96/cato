from dataclasses import dataclass


@dataclass
class BranchName:
    name: str

    def __str__(self):
        return self.name
