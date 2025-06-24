#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import xml.etree.ElementTree as ET
from run_scan import Block, Cell


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


def get_geometry(block: Block) -> Cell:
    """Traverse Block tree, return the geometry"""

    pass


def build_xml(svg: ET.Element, block: Block, cell: Cell) -> tuple[ET.Element, Cell]:
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

    for child in block.children:
        build_xml(svg, child, cell)
    # svg.set("viewBox", f"0 0 {x + rect_width} {y + rect_height}")
    return svg
