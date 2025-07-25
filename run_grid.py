#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Optional
from dataclasses import dataclass, field
import glob
import argparse
import pickle
import argcomplete
from run_scan import Block, Cell  # noqa: F401


parser = argparse.ArgumentParser(
    description="Convert tree of Block -s to array",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)


@dataclass
class Node:
    row: int = 0
    column: int = 0
    color: str = ""
    text: str = ""
    depth: int = 0
    tags: list[str] = field(default_factory=list)

    def __str____(self):
        return f"[{self.row}, {self.column}] {self.color!r}: {self.text!r}"


# GridType = list[list[Optional[Node]]]
GridType = list[list[Node]]


def build_grid(
    block: Block, grid: GridType = [[]], last: Cell = Cell(0, 0)
) -> tuple[GridType, Cell]:
    row, column = block.cell.row, block.cell.column
    while last.row < row:
        grid.append([])
        last.row += 1
    while last.column < column:
        grid[row].append(Node(row, column))
        last.column += 1
    grid[row].append(
        Node(row, column, block.color, block.text, block.depth, block.tags)
    )
    for child in block.children:
        _cell: Cell
        _, _cell = build_grid(child, grid, last.dup())
        last = _cell.dup()
        last.column += 1
    return grid, last


if __name__ == "__main__":
    argcomplete.autocomplete(parser)
    parser.add_argument(
        "pickle", help="Select .picle file to import", choices=glob.glob("*.pickle")
    )
    args = parser.parse_args()
    block: Block
    with open(args.pickle, "rb") as pickle_file:
        block = pickle.load(pickle_file)
    grid: GridType = build_grid(block, [[]], Cell(0, 0))[0]
    print(grid)
