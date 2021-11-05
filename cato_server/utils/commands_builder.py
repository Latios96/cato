from typing import List


class CommandsBuilder:
    def __init__(self, base_command: str, max_length: int):
        self._commands = []
        self._base_command = base_command
        self._init_current_command()
        self._max_length = max_length

    def push(self, part_str: str):
        complete_length = len(self._current_command) + len(part_str)

        max_length_not_exceeded = complete_length < self._max_length
        if max_length_not_exceeded:
            self._push_to_current_command(part_str)
            return

        self._commands.append(self._current_command)
        self._init_current_command()
        self._push_to_current_command(part_str)

    def finalize(self) -> List[str]:
        self._commands.append(self._current_command)
        return self._commands

    def _init_current_command(self):
        self._current_command = self._base_command

    def _push_to_current_command(self, part_str):
        self._current_command += part_str
