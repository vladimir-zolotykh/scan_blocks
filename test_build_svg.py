#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os
import subprocess


file_str = """\
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"
    "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" width="342" height="216" viewBox="0 0 114 72"><rect x="0px" y="0px" width="342" height="216" fill="lightgray" /><rect x="1" y="1" width="36" height="10" fill="#00CCDE" stroke="black" /><text x="19" y="8" text-anchor="middle" font-size="4">Messagebox Window </text><rect x="39" y="1" width="36" height="10" fill="lightgray" stroke="None" /><text x="57" y="8" text-anchor="middle" font-size="4" /><rect x="77" y="1" width="36" height="10" fill="lightgray" stroke="None" /><text x="95" y="8" text-anchor="middle" font-size="4" /><rect x="1" y="13" width="36" height="10" fill="lightgray" stroke="None" /><text x="19" y="20" text-anchor="middle" font-size="4">Frame  </text><rect x="39" y="13" width="36" height="10" fill="lightgray" stroke="None" /><text x="57" y="20" text-anchor="middle" font-size="4" /><rect x="77" y="13" width="36" height="10" fill="lightgray" stroke="None" /><text x="95" y="20" text-anchor="middle" font-size="4" /><rect x="1" y="25" width="36" height="10" fill="lightgray" stroke="None" /><text x="19" y="32" text-anchor="middle" font-size="4" /><rect x="39" y="25" width="36" height="10" fill="White" stroke="black" /><text x="57" y="32" text-anchor="middle" font-size="4">Message text</text><rect x="77" y="25" width="36" height="10" fill="lightgray" stroke="None" /><text x="95" y="32" text-anchor="middle" font-size="4" /><rect x="1" y="37" width="36" height="10" fill="lightgray" stroke="None" /><text x="19" y="44" text-anchor="middle" font-size="4" /><rect x="39" y="37" width="36" height="10" fill="lightgray" stroke="None" /><text x="57" y="44" text-anchor="middle" font-size="4" /><rect x="77" y="37" width="36" height="10" fill="lightgray" stroke="None" /><text x="95" y="44" text-anchor="middle" font-size="4" /><rect x="1" y="49" width="36" height="10" fill="goldenrod" stroke="black" /><text x="19" y="56" text-anchor="middle" font-size="4">OK Button</text><rect x="39" y="49" width="36" height="10" fill="lightgray" stroke="None" /><text x="57" y="56" text-anchor="middle" font-size="4" /><rect x="77" y="49" width="36" height="10" fill="#ff0505" stroke="black" /><text x="95" y="56" text-anchor="middle" font-size="4">Cancel Button</text><rect x="1" y="61" width="36" height="10" fill="lightgray" stroke="None" /><text x="19" y="68" text-anchor="middle" font-size="4" /><rect x="39" y="61" width="36" height="10" fill="lightgray" stroke="None" /><text x="57" y="68" text-anchor="middle" font-size="4" /><rect x="77" y="61" width="36" height="10" fill="lightgray" stroke="None" /><text x="95" y="68" text-anchor="middle" font-size="4" /></svg>"""


def test_file():
    # Run the script
    os.remove("message.svg")
    subprocess.run(["python", "build_svg.py", "message.blk"], check=True)

    # Read and compare output
    with open("message.svg") as f:
        s = f.read()

    assert s == file_str
