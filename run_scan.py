#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import pprint


class InvalidState(TypeError):
    pass


@dataclass
class Block:
    # color: str
    # text: str
    body: list[str] = field(default_factory=list)
    children: list[Block] = field(default_factory=list)


State = Enum("State", ["start", "in_", "out", "end"])


def parse_block(
    buffer: str,
    cursor: int = 0,
    state: State = State.out,
) -> Block:
    offset: int
    block: Block
    for offset in range(cursor, len(buffer)):
        ch: str = buffer[offset]
        if ch == "[":
            if state == State.out:
                state = State.in_
                block = Block()
            elif state == State.in_:
                block.children.append(parse_block(buffer, offset + 1))
            else:
                raise InvalidState()
        elif ch == "]":
            if state == State.in_:
                return block
            else:
                raise InvalidState()
        else:
            if state == State.in_:
                block.body.append(ch)
            else:
                raise InvalidState()
    return block


if __name__ == "__main__":
    with open("message.blk") as input:
        # type(input):   <class '_io.TextIOWrapper'>
        buffer: str = input.read()
        block: Block
        block = parse_block(buffer)
        pprint.pprint(f"{block = }")
