from dataclasses import dataclass


@dataclass
class Resolution:
    width: int
    height: int

    def __post_init__(self):
        if self.width < 0:
            raise ValueError("Width can not be smaller than 0!")
        if self.height < 0:
            raise ValueError("Height can not be smaller than 0!")

    def __str__(self):
        return f"{self.width}x{self.height}px"
