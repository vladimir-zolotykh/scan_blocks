#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> ps = ParserState()
>>> ps
ParserState(buffer=None, offset=None, state=None)
>>> with open("lightgray.blk") as f:
...     lightgray_str = f.read()
...
>>> lightgray_str
'[lightgray: Frame\\n    [] [White: Message text]\\n    //\\n    [goldenrod: OK Button] [] [#ff0505: Cancel Button]\\n    /\\n    []\\n]\\n'
>>> lines = find_line_boundaries(lightgray_str)
>>> lines
{1: (0, 18), 2: (18, 29), 3: (47, 7), 4: (54, 55), 5: (109, 6), 6: (115, 7), 7: (122, 2)}
>>> which_line(47, lines)
3
>>> which_line(10, lines)
1
>>> which_line(17, lines)
1
"""

from typing import Optional
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
    buffer: Optional[str] = None
    offset: Optional[int] = None
    state: Optional[State] = None

    def make_error(self) -> None:
        raise InvalidState(self.offset, self.state, "Invalid state")

    def offset2line_number(self) -> int:
        return 0

    def log_current_line(self) -> None:
        logging.info(f"{self.buffer = }, {self.offset = }, {self.state = }")


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


def which_line(char_no: int, lines: dict[int, tuple[int, int]]) -> int:
    """Return the line that has CHAR_NO"""

    for line_no in lines:
        val = lines[line_no]
        if char_no in range(val[0], val[0] + val[1]):
            return line_no
    return -1  # not found


if __name__ == "__main__":
    import doctest

    doctest.testmod()
