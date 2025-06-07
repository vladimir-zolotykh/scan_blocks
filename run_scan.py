#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import pprint

State = Enum("State", ["start", "in_", "out", "end"])


class InvalidState(Exception):
    def __init__(
        self, cursor: int, state: State, message: str = "Invalid state"
    ) -> None:
        super().__init__(f"{cursor = }: {message = } {state = }")


@dataclass
class Block:
    # color: str
    # text: str
    body: list[str] = field(default_factory=list)
    children: list[Block] = field(default_factory=list)

    def __repr__(self):
        return f"Block(body={''.join(self.body)}, children=({self.children}))"


def parse_block(
    buffer: str,
    cursor: int = 0,
    state: State = State.out,
) -> Block:
    def make_error() -> None:
        raise InvalidState(cursor, state, "Invalid state")

    offset: int
    block: Block = Block()
    for offset in range(cursor, len(buffer)):
        ch: str = buffer[offset]
        if ch == "[":
            if state == State.out:
                state = State.in_
            elif state == State.in_:
                block.children.append(parse_block(buffer, offset + 1, state=State.in_))
            else:
                make_error()
        elif ch == "]":
            if state == State.in_:
                return block
            else:
                make_error()
        else:
            if state == State.in_:
                block.body.append(ch)
            else:
                make_error()
    return block


if __name__ == "__main__":
    with open("message.blk") as input:
        # type(input):   <class '_io.TextIOWrapper'>
        buffer: str = input.read()
        block: Block
        block = parse_block(buffer)
        print(repr(block))
        # pprint.pprint(f"{block = }")
