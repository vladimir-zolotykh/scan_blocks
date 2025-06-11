#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import glob
import argparse
import argcomplete
import re
import pprint

State = Enum("State", ["void", "in_", "out", "new_line"])


class InvalidState(Exception):
    def __init__(
        self, cursor: int, state: State, message: str = "Invalid state"
    ) -> None:
        super().__init__(f"{cursor = }: {message = } {state = }")


body_re = re.compile(
    r"""
\s*
(?P<color>\#[\dA-Fa-f]{6}|[a-zA-Z]\w*):
\s*
(?P<text>\w+)
\s*""",
    re.VERBOSE | re.MULTILINE | re.DOTALL,
)


@dataclass
class Cell:
    row: int = 0
    column: int = 0

    def dup(self) -> Cell:
        return Cell(self.row, self.column)

    def next_row(self) -> Cell:
        return Cell(self.row + 1, self.column)

    def next_column(self) -> Cell:
        return Cell(self.row, self.column + 1)

    def __repr__(self) -> str:
        return f"Cell({self.row}, {self.column})"


@dataclass
class Block:
    color: str = ""
    text: str = ""
    cell: Cell = field(default_factory=Cell)
    _body: list[str] = field(default_factory=list)
    children: list[Block] = field(default_factory=list)

    @property
    def body_str(self) -> str:
        return "".join(self._body)

    def append_ch(self, ch: str) -> None:
        self._body.append(ch)

    def __repr__(self):
        result = "Block("
        result += repr(self.cell)
        if self._body:
            result += ", "
            match = body_re.match(self.body_str)
            if match:
                color, text = match.groups()
                result += f"color={color}"
                if text:
                    result += f", text={text}"
            else:
                result += f"body={self.body_str}"
        if self.children:
            result += f", children={self.children}"
        result += ")"
        return result


def parse_block(
    buffer: str,
    cursor: int = 0,
    cell: Cell = Cell(0, 0),
    state: State = State.out,
) -> tuple[Block, int]:
    """Parse block ([])

    returns Block, input buffer offset, Cell (row, column pointer)"""

    def make_error() -> None:
        raise InvalidState(cursor, state, "Invalid state")

    offset: int = cursor
    block: Block = Block(cell=cell.dup())
    while offset < len(buffer):
        ch: str = buffer[offset]
        if ch == "[":
            if state == State.out:
                state = State.in_
            elif state == State.in_:
                _block: Block
                _block, offset = parse_block(
                    buffer,
                    offset + 1,
                    cell,
                    state=State.in_,
                )
                cell.column += 1
                block.children.append(_block)
            else:
                make_error()
        elif ch == "]":
            if state == State.in_:
                return block, offset
            else:
                make_error()
        elif ch == "/":
            if state == State.new_line:
                # eat second "/"
                state = State.in_
            else:
                state = State.new_line
                cell.row += 1
                cell.column = 0
        else:
            if state == State.in_:
                block.append_ch(ch)
            else:
                make_error()
        offset += 1
    # We never reach the following return statement
    assert True, "Can't happen"
    return block, offset


parser = argparse.ArgumentParser(
    description="Parse .blk file",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
if __name__ == "__main__":
    parser.add_argument("file_to_parse", choices=glob.glob("*.blk"))
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    found_blk_files: list[str] = []
    with open(args.file_to_parse) as input:
        # type(input):   <class '_io.TextIOWrapper'>
        buffer: str = input.read()
        block: Block
        block = parse_block(buffer, 0, Cell(0, 0))[0]
        pprint.pprint(repr(block))
