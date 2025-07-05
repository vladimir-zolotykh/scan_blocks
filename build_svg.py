#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import NamedTuple, Optional
import xml.etree.ElementTree as ET
import glob
import argparse
import argcomplete
import run_scan as RS
import run_grid as RG

screen_width = 1280
screen_height = 1024
canvas_width = f"{screen_width // 3}px"
canvas_height = f"{screen_height // 3}px"
view_width = 108
view_height = 70


def init_svg_root(
    view_width: int = 114, view_height: int = 84, factor: int = 3
) -> ET.Element:
    svg_root = ET.Element(
        "svg",
        {
            "xmlns": "http://www.w3.org/2000/svg",
            "xmlns:xlink": "http://www.w3.org/1999/xlink",
            "xml:space": "preserve",
            "width": str(view_width * factor),
            "height": str(view_height * factor),
            "viewBox": f"0 0 {view_width} {view_height}",
        },
    )
    background = ET.Element(
        "rect",
        {
            "x": "0px",
            "y": "0px",
            "width": str(view_width * factor),
            "height": str(view_height * factor),
            "fill": "lightgray",
        },
    )
    svg_root.insert(0, background)
    return svg_root


rect_width: int = 36
rect_height: int = 10
font_size: int = 4
x_spacing: int = 36
stroke_thickness = 1


def get_size(grid: RG.GridType) -> tuple[int, int]:
    """Return size (columns, rows) of `grid'"""

    rows: int = len(grid)
    columns: int = 0
    for row in grid:
        if columns < len(row):
            columns = len(row)
    return columns, rows


def sub_rect(
    svg_root: ET.Element,
    x: int,
    y: int,
    text: str,
    fill: str = "None",
    stroke: str = "black",
    width: int = rect_width,
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
            "font-size": str(font_size),
        },
    ).text = text


class Point(NamedTuple):
    x: int
    y: int


def rect_start(column: int, row: int) -> Point:
    """Return top-left corner of rectangle

    converts column, row to pixel"""

    return Point(_get1_x(column), _get1_y(row))


def rect_end(column: int, row: int) -> Point:
    """Return bottom-right corner (next to it) of rectangle

    converts column, row to pixel"""

    return Point(_get2_x(column), _get2_y(row))


def _get1_x(column: int, v: int = stroke_thickness, w: int = rect_width) -> int:
    if column == 0:
        return v
    else:
        return _get1_x(column - 1) + w + v + v


def _get2_x(column: int, v: int = stroke_thickness, w: int = rect_width) -> int:
    return _get1_x(column) + w + v


def _get1_y(row: int, v: int = stroke_thickness, h: int = rect_height) -> int:
    if row == 0:
        return v
    else:
        return _get1_y(row - 1) + h + v + v


def _get2_y(row: int, v: int = stroke_thickness, h: int = rect_height) -> int:
    return _get1_y(row) + h + v


def build_svg(grid: RG.GridType) -> ET.Element:
    x: int = 0
    y: int = 0
    v: int = stroke_thickness
    width: int
    columns, rows = get_size(grid)
    svg_root: ET.Element = init_svg_root(columns * 38, rows * 12, 3)
    node: Optional[RG.Node]
    for row_index in range(rows):
        for column_index in range(columns):
            x, y = rect_start(column_index, row_index)
            # y, x = get_xy(row_index, column_index)
            try:
                node = grid[row_index][column_index]
                assert isinstance(node, RG.Node)
                if node.color == "":
                    node.color = "lightgray"
            except IndexError:
                node = RG.Node(row_index, column_index, "lightgray")
            fill, text = node.color, node.text
            if fill == "":
                fill = "None"
            stroke = "black"
            if ":nostroke" in node.tags or text.strip() == "":
                stroke = "None"
            if ":center" in node.tags:
                width = rect_width * columns + 2 * v
            else:
                width = rect_width + 2 * v
            width = rect_width
            sub_rect(svg_root, x, y, text, fill, stroke, width)
    # _view_width, _view_height = rect_end(columns, rows)
    # svg_root.set("viewBox", "0 0 115, 84")
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
    # build_svg(grid)
    tree = ET.ElementTree(build_svg(grid))
    with open("message.svg", "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
        f.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"\n')
        f.write('    "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n')
        tree.write(f, encoding="unicode")
