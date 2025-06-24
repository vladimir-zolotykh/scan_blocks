#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import xml.etree.ElementTree as ET
import glob
import argparse
import argcomplete
import run_scan as RS
import run_grid as RG


svg_root = ET.Element(
    "svg",
    {
        "xmlns": "http://www.w3.org/2000/svg",
        "xmlns:xlink": "http://www.w3.org/1999/xlink",
        "xml:space": "preserve",
        "width": "432px",
        "height": "240px",
        "viewBox": "0 0 108 60",
    },
)
rect_width: int = 36
rect_height: int = 10
font_size: int = 5
x_spacing: int = 36
y_offset: int = 10


def get_size(grid: RG.GridType) -> tuple[int, int]:
    """Return size (columns, rows) of `grid'"""

    rows: int = len(grid)
    columns: int = 0
    for row in grid:
        if columns < len(row):
            columns = len(row)
    return columns, rows


def build_svg(grid: RG.GridType) -> ET.Element:
    print(get_size(grid))
    y: int = y_offset + cell.row * rect_height
    x: int = cell.column * x_spacing
    fill, text = block.color, block.text
    ET.SubElement(
        svg,
        "rect",
        {
            "x": str(x),
            "y": str(y),
            "width": str(rect_width),
            "height": str(rect_height),
            "fill": fill,
            "stroke": "black",
        },
    )
    ET.SubElement(
        svg,
        "text",
        {
            "x": str(x + rect_width // 2),
            "y": str(y + rect_height - 3),
            "text-anchor": "middle",
            "font-size": str(font_size),
        },
    ).text = text

    # svg.set("viewBox", f"0 0 {x + rect_width} {y + rect_height}")
    return svg


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
    svg = build_svg(grid)
    print(svg)
