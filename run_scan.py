#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from dataclasses import dataclass, field
import glob
import argparse
import argcomplete
import re
import pprint
import logging
import parser_state as PS


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
    state: PS.State = PS.State.out,
    depth: int = 0,
) -> tuple[Block, int]:
    """Parse block ([])

    returns Block, input buffer offset, Cell (row, column pointer)"""
    offset: int = cursor
    block: Block = Block(cell=cell.dup())
    ps: PS.ParserState = PS.ParserState(buffer, offset, state)
    while offset < len(buffer):
        ch: str = buffer[offset]
        if ch == "[":
            if state == PS.State.out:
                state = PS.State.in_
            elif state == PS.State.in_:
                _block: Block
                _block, offset = parse_block(
                    buffer, offset + 1, cell, state=PS.State.in_, depth=depth + 1
                )
                cell.column += 1
                block.children.append(_block)
            else:
                ps.make_error()
        elif ch == "]":
            if state == PS.State.in_:
                if 0 < depth:
                    return block, offset
                else:
                    pass  # continue paring
            else:
                ps.make_error()
        elif ch == "/":
            if state == PS.State.new_line:
                # eat second "/"
                state = PS.State.in_
            else:
                state = PS.State.new_line
                cell.row += 1
                cell.column = 0
        elif ch == "\n":
            # "/" instead of "//"
            if state == PS.State.new_line:
                state = PS.State.in_
            else:
                ps.log_current_line()
                cell.row += 1
        else:
            if state == PS.State.in_:
                block.append_ch(ch)
            else:
                ps.make_error()
        offset += 1
    return block, offset


parser = argparse.ArgumentParser(
    description="Parse .blk file",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
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
