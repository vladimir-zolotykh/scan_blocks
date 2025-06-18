#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import glob
import argparse
import pickle
import argcomplete
from run_scan import Block, Cell  # noqa: F401


parser = argparse.ArgumentParser(
    description="Convert tree of Block -s to array",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)


if __name__ == "__main__":
    argcomplete.autocomplete(parser)
    parser.add_argument(
        "pickle", help="Select .picle file to import", choices=glob.glob("*.pickle")
    )
    args = parser.parse_args()
    block: Block
    with open(args.pickle, "rb") as pickle_file:
        block = pickle.load(pickle_file)
    print(block)
