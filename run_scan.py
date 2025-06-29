#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
import os
from dataclasses import dataclass, field
import glob
import argparse
import argcomplete
import re
import logging
import pickle
from parser_state import ParserState, State


# fmt: off
body_re = re.compile(r"""\s*
                         (?P<color>\#[\dA-Fa-f]{6}|[a-zA-Z]\w*):
                         \s*
                         (?P<text>[^][\n]+)
                         \s*""",
                     re.VERBOSE)
# fmt: on


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


def extract_tags(
    text: str, tags: tuple[str, ...] = (":nostroke", ":center")
) -> tuple[str, list[str]]:
    """Modify TEXT string.

    Remove :nostroke, :center from it. Return modified string and found tags"""

    found: list[str] = []
    for tag in tags:
        if tag in text:
            text = text.replace(tag, "")
            found.append(tag)
    return text, found


@dataclass
class Block:
    _color: str = ""
    _text: str = ""
    cell: Cell = field(default_factory=Cell)
    _body: list[str] = field(default_factory=list)
    children: list[Block] = field(default_factory=list)
    depth: int = 0
    tags: list[str] = field(default_factory=list)

    @property
    def color(self):
        return self._color

    @property
    def text(self):
        return self._text

    @property
    def body_str(self) -> str:
        return "".join(self._body)

    def init_text(self) -> Block:
        """Extract COLOR, TEXT stromgs from body_str

        Set corresponding class attributes"""
        match = body_re.match(self.body_str)
        if match:
            color, text = match.groups()
            if color:
                self._color = color
            if text:
                self._text, self.tags = extract_tags(text)
        return self

    def append_ch(self, ch: str) -> None:
        self._body.append(ch)

    def __repr__(self):
        result = "Block("
        result += repr(self.cell)
        if self._body:
            result += ", "
            self.init_text()
            if self.color:
                result += f'color="{self.color}"'
            if self.text:
                result += f', text="{self.text}"'
            else:
                result += f'body="{self.body_str}"'
        if self.children:
            result += f", children={self.children}"
        result += ")"
        return result


state_history: list[State] = []


def track_state(state: State) -> State:
    state_history.append(state)
    return state


def parse_block(
    buffer: str,
    cursor: int = 0,
    cell: Cell = Cell(0, 0),
    state: State = State.void,
    depth: int = 0,
) -> tuple[Block, int]:
    """Parse block ([])

    returns Block, input buffer offset, Cell (row, column pointer)"""
    offset: int = cursor
    block: Block = Block(cell=cell.dup(), depth=depth)
    while offset < len(buffer):
        ch: str = buffer[offset]
        if ch == "[":
            if state == State.void:
                state = track_state(State.in_)
            elif state == State.in_:
                _block: Block
                _block, offset = parse_block(
                    buffer,
                    offset + 1,
                    cell,
                    state=track_state(State.in_),
                    depth=depth + 1,
                )
                cell.column += 1
                block.children.append(_block.init_text())
            else:
                ParserState(buffer, offset, state).make_error()
        elif ch == "]":
            if state == State.in_:
                if 0 < depth:
                    return block, offset
                else:
                    pass  # continue paring
            else:
                ParserState(buffer, offset, state).make_error()
        elif ch == "/":
            if state == State.new_line:
                # eat second "/"
                state = track_state(State.in_)
            else:
                state = track_state(State.new_line)
                # cell.row += 1
                cell.column = 0
        elif ch == "\n":
            # "/" instead of "//"
            if state == State.new_line:
                state = track_state(State.in_)
            else:
                if state != State.in_:
                    ParserState(buffer, offset, state).make_error()
                block.append_ch(ch)
                ParserState(buffer, offset, state).log_current_line()
                cell.row += 1
        else:
            if state == State.in_:
                block.append_ch(ch)
            else:
                ParserState(buffer, offset, state).make_error()
        offset += 1
    return block.init_text(), offset


parser = argparse.ArgumentParser(
    description="Parse .blk file",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "--pickle",
    action="store_true",
    help=" Pickle Block object in a file",
)
if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    parser.add_argument("file_to_parse", choices=glob.glob("*.blk"))
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    found_blk_files: list[str] = []
    block: Block
    with open(args.file_to_parse) as input:
        buffer: str = input.read()
        block = parse_block(buffer, 0, Cell(0, 0), track_state(State.void))[0]
    if args.pickle:
        pickle_filename = (
            os.path.splitext(os.path.basename(args.file_to_parse))[0] + ".pickle"
        )
        with open(pickle_filename, "wb") as pickle_descriptor:
            pickle.dump(block, pickle_descriptor)
            print(f"Block saved in {pickle_filename}")
    print(state_history)
    print(block)
