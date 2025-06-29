#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import sys
from typing import Optional
import xml.etree.ElementTree as ET
import glob
import argparse
import argcomplete
import run_scan as RS
import run_grid as RG

canvas_width = "432px"
canvas_height = "240px"
view_width = 108
view_height = 70

svg_root = ET.Element(
    "svg",
    {
        "xmlns": "http://www.w3.org/2000/svg",
        "xmlns:xlink": "http://www.w3.org/1999/xlink",
        "xml:space": "preserve",
        "width": canvas_width,
        "height": canvas_height,
        "viewBox": f"0 0 {view_width} {view_height}",
    },
)
background = ET.Element(
    "rect",
    {
        "x": "0px",
        "y": "0px",
        "width": canvas_width,
        "height": canvas_height,
        "fill": "lightgray",
    },
)
svg_root.insert(0, background)
rect_width: int = 36
rect_height: int = 10
font_size: int = 5
x_spacing: int = 36


def get_size(grid: RG.GridType) -> tuple[int, int]:
    """Return size (columns, rows) of `grid'"""

    rows: int = len(grid)
    columns: int = 0
    for row in grid:
        if columns < len(row):
            columns = len(row)
    return columns, rows


def sub_rect(
    x: int,
    y: int,
    text: str,
    fill: str = "None",
    stroke: str = "None",
    width: int = rect_width,
    tags: list[str] = [],
) -> None:
    ET.SubElement(
        svg_root,
        "rect",
        {
            "x": str(x),
            "y": str(y),
            "width": str(width),
            "height": str(rect_height),
            "fill": fill,
            "stroke": stroke,
        },
    )
    ET.SubElement(
        svg_root,
        "text",
        {
            "x": str(x + width // 2),
            "y": str(y + rect_height - 3),
            "text-anchor": "middle",
            "font-size": str(font_size - 1),
        },
    ).text = text


def build_svg(grid: RG.GridType) -> ET.Element:
    x: int = 0
    y: int = 0
    columns, rows = get_size(grid)
    row: list[Optional[RG.Node]]
    node: Optional[RG.Node]
    for row_index, row in enumerate(grid):
        for column_index, node in enumerate(row):
            y = row_index * rect_height
            x = column_index * x_spacing
            assert node
            fill, text, depth, tags = node.color, node.text, node.depth, node.tags
            if fill == "":
                fill = "None"
            stroke = "black" if text else "None"
            _width: int = rect_width
            # handle [#00CCDE: Messagebox Window
            _width = rect_width * columns if len(row) == 1 else rect_width
            if depth == 1:  # [lightgray: Frame
                stroke = "None"
                # fill = "None"
            sub_rect(x, y, text, fill, stroke, _width, tags)

    svg_root.set("viewBox", f"0 0 {rect_width * columns} {rect_height * rows}")
    return svg_root


parser = argparse.ArgumentParser(
    description="Build SVG from .blk file",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

if __name__ == "__main__":
    parser.add_argument(
        "blk_file", help=".blk file to convert to SVG", choices=glob.glob("*.blk")
    )
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    block: RS.Block
    with open(args.blk_file) as f:
        buf: str = f.read()
        block = RS.parse_block(buf, 0, RS.Cell(0, 0))[0]
    grid: RG.GridType = RG.build_grid(block, [[]], RS.Cell(0, 0))[0]
    build_svg(grid)
    tree = ET.ElementTree(svg_root)
    with open("message.svg", "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
        f.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"\n')
        f.write('    "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n')
        tree.write(f, encoding="unicode")
