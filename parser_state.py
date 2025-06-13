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
>>>
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


if __name__ == "__main__":
    import doctest

    doctest.testmod()
