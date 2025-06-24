#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> import run_scan as RS
>>> import run_grid as RG
>>> import parser_state as PS
>>> with open("message.blk") as f:
...     buf = f.read()
...     blk = RS.parse_block(buf, 0, RS.Cell(0, 0), RS.track_state(PS.State.void))[0]
...
>>> blk
Block(Cell(0, 0), color="#00CCDE", text="Messagebox Window", \
children=[Block(Cell(1, 0), color="lightgray", text="Frame", children=[Block(Cell(2, 0)), \
Block(Cell(2, 1), color="White", text="Message text"), \
Block(Cell(4, 0), color="goldenrod", text="OK Button"), \
Block(Cell(4, 1)), Block(Cell(4, 2), color="#ff0505", text="Cancel Button"), \
Block(Cell(5, 0))])])
>>> RS.state_history
[<State.void: 1>, <State.in_: 2>, <State.in_: 2>, <State.in_: 2>, \
<State.in_: 2>, <State.new_line: 4>, <State.in_: 2>, <State.in_: 2>, \
<State.in_: 2>, <State.in_: 2>, <State.new_line: 4>, <State.in_: 2>, \
<State.in_: 2>]
>>> import pickle
>>> import run_grid as RG
>>> with open("message.pickle", "rb") as f:
...     blk = pickle.load(f)
...
>>> grid = RG.build_grid(blk, [[]], RS.Cell(0, 0))[0]
>>> grid
[[Node(row=0, column=0, color='#00CCDE', text='Messagebox Window')], \
[Node(row=1, column=0, color='lightgray', text='Frame')], \
[Node(row=2, column=0, color='', text=''), \
Node(row=2, column=1, color='White', text='Message text')], [], \
[Node(row=4, column=0, color='goldenrod', text='OK Button'), \
Node(row=4, column=1, color='', text=''), \
Node(row=4, column=2, color='#ff0505', text='Cancel Button')], \
[Node(row=5, column=0, color='', text='')]]

"""

if __name__ == "__main__":
    import doctest
    from run_scan import Block, Cell  # noqa: F401

    doctest.testmod()
