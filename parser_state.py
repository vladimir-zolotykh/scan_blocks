#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> ps = ParserState()
>>> ps
ParserState(buffer='', offset=0, state=<State.void: 1>)
>>> with open("lightgray.blk") as f:
...     lightgray_str = f.read()
...
>>> lightgray_str
'[lightgray: Frame\\n    [] [White: Message text]\\n    //\\n    \
[goldenrod: OK Button] [] [#ff0505: Cancel Button]\\n    /\\n    []\\n]\\n'
>>> lines = ps.find_line_boundaries(lightgray_str)
>>> lines
{1: (0, 18), 2: (18, 29), 3: (47, 7), 4: (54, 55), 5: (109, 6), 6: (115, 7),\
 7: (122, 2)}
>>> ps.which_line(47, lines)
3
>>> ps.which_line(10, lines)
1
>>> ps.which_line(17, lines)
1
"""

from dataclasses import dataclass
from enum import Enum
import logging

State = Enum("State", ["void", "in_", "out", "new_line"])


class InvalidState(Exception):
    def __init__(
        self, cursor: int, state: State, message: str = "Invalid state"
    ) -> None:
        super().__init__(f"{cursor = }: {message = } {state = }")


@dataclass
class ParserState:
    buffer: str = ""
    offset: int = 0
    state: State = State.void

    def make_error(self) -> None:
        raise InvalidState(self.offset, self.state, "Invalid state")

    def log_current_line(self) -> None:
        lines: dict[int, tuple[int, int]] = self.find_line_boundaries(self.buffer)
        line_no: int = self.which_line(self.offset, lines)
        logging.info(f"{self.offset = }, {line_no = }, {self.state = }")

    @staticmethod
    def which_line(char_no: int, lines: dict[int, tuple[int, int]]) -> int:
        """Return the line that has CHAR_NO"""

        for line_no in lines:
            val = lines[line_no]
            if char_no in range(val[0], val[0] + val[1]):
                return line_no
        return -1  # not found

    @staticmethod
    def find_line_boundaries(buffer: str) -> dict[int, tuple[int, int]]:
        """Return a mapping of char postion to line number"""

        line_no: int = 1
        line_start: int = 0
        line_len: int = 0
        lines: dict[int, tuple[int, int]] = {}
        for char_no in range(len(buffer)):
            line_len += 1  # "\n" is last char of any line
            if buffer[char_no] == "\n":
                lines[line_no] = (line_start, line_len)
                line_no += 1
                line_start = char_no + 1
                line_len = 0
        return lines


if __name__ == "__main__":
    import doctest

    doctest.testmod()
