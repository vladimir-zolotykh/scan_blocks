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

State = Enum("State", ["start", "in_", "out", "end"])


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
class Block:
    color: str = ""
    text: str = ""
    _body: list[str] = field(default_factory=list)
    children: list[Block] = field(default_factory=list)

    @property
    def body(self) -> list[str]:
        return self._body

    def __repr__(self):
        result = "Block("
        if self.body:
            body_str = "".join(self._body)
            match = body_re.match(body_str)
            if match:
                color, text = match.groups()
                result += f"color={color}"
                if text:
                    result += f", text={text}"
            else:
                result += f"body={body_str}"
        if self.children:
            result += f", children={self.children}"
        result += ")"
        return result


def parse_block(
    buffer: str,
    cursor: int = 0,
    state: State = State.out,
) -> tuple[Block, int]:
    def make_error() -> None:
        raise InvalidState(cursor, state, "Invalid state")

    offset: int = cursor
    block: Block = Block()
    while offset < len(buffer):
        ch: str = buffer[offset]
        if ch == "[":
            if state == State.out:
                state = State.in_
            elif state == State.in_:
                _block: Block
                _block, _offset = parse_block(buffer, offset + 1, state=State.in_)
                offset = _offset
                block.children.append(_block)
            else:
                make_error()
        elif ch == "]":
            if state == State.in_:
                return block, offset
            else:
                make_error()
        else:
            if state == State.in_:
                block.body.append(ch)
            else:
                make_error()
        offset += 1
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
        block, _ = parse_block(buffer)
        print(repr(block))
        # pprint.pprint(f"{block = }")
