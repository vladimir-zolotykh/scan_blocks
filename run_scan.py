#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
import typing
from dataclasses import dataclass, field


@dataclass
class Block:
    color: str
    test: str
    children: list[Block] = field(default_factory=list)


PAIRS = list[tuple[int, int]]


def find_open_bracket(buffer: str, cursor: int) -> PAIRS:
    blocks: PAIRS = []
    return blocks


if __name__ == "__main__":
    with open("message.blk") as input:
        # type(input):   <class '_io.TextIOWrapper'>
        buffer: str = input.read()
        print(f"{buffer = }")
