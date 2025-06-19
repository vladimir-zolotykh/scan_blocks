#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Optional
import glob
import argparse
import pickle
import argcomplete
from run_scan import Block, Cell  # noqa: F401


parser = argparse.ArgumentParser(
    description="Convert tree of Block -s to array",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

GridType = list[list[Optional[Block]]]


def build_grid(
    block: Block, grid: GridType = list([]), last: Cell = Cell(0, 0)
) -> GridType:
    row, column = block.cell.row, block.cell.column
    print(f"{row = }, {column = }, {last = }")
    while last.row < row:
        grid.append(list())
        last.row += 1
    while last.column < column:
        grid[-1].append(None)
        last.column += 1
    grid[-1].append(block)
    grid.append(list())
    last.row += 1
    for child in block.children:
        build_grid(child, grid, last.dup())
        last.column += 1
    return grid


if __name__ == "__main__":
    argcomplete.autocomplete(parser)
    parser.add_argument(
        "pickle", help="Select .picle file to import", choices=glob.glob("*.pickle")
    )
    args = parser.parse_args()
    block: Block
    with open(args.pickle, "rb") as pickle_file:
        block = pickle.load(pickle_file)
    grid: GridType = build_grid(block)
    print(grid)
