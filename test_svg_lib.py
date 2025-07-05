#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest
from build_svg import _get1_x, _get1_y, _get2_x, _get2_y
from build_svg import Point, rect_start, rect_end

xy_table = (
    (0, 0, (1, 1), (38, 12)),
    (0, 1, (39, 1), (76, 12)),
    (0, 2, (77, 1), (114, 12)),
    (1, 0, (1, 13), (38, 24)),
    (1, 1, (39, 13), (76, 24)),
    (1, 2, (77, 13), (114, 24)),
    (2, 0, (1, 25), (38, 36)),
    (2, 1, (39, 25), (76, 36)),
    (2, 2, (77, 25), (114, 36)),
    (3, 0, (1, 37), (38, 48)),
    (3, 1, (39, 37), (76, 48)),
    (3, 2, (77, 37), (114, 48)),
    (4, 0, (1, 49), (38, 60)),
    (4, 1, (39, 49), (76, 60)),
    (4, 2, (77, 49), (114, 60)),
    (5, 0, (1, 61), (38, 72)),
    (5, 1, (39, 61), (76, 72)),
    (5, 2, (77, 61), (114, 72)),
)


@pytest.mark.parametrize(
    "row, col, x1_y1, x2_y2", xy_table, ids=[f"row{r}_col{c}" for r, c, *_ in xy_table]
)
def test_get_xy(row, col, x1_y1, x2_y2):
    assert (_get1_x(col), _get1_y(row)) == x1_y1
    assert (_get2_x(col), _get2_y(row)) == x2_y2


@pytest.mark.parametrize(
    "row, col, xy1, xy2", xy_table, ids=[f"row{r}_col{c}" for r, c, *_ in xy_table]
)
def test_rect(row, col, xy1, xy2):
    assert rect_start(col, row) == Point(*xy1)
    assert rect_end(col, row) == Point(*xy2)
