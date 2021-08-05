from dataclasses import dataclass

import humanfriendly


@dataclass
class MachineInfo:
    cpu_name: str
    cores: int
    memory: float

    @property
    def memory_str(self):
        return humanfriendly.format_size(self.memory)
