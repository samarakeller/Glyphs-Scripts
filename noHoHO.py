#MenuTitle: no HOHO
# -*- coding: utf-8 -*-
__doc__ = """
Inserts n, o, H, O after every character in the current Edit view text.
"""

import GlyphsApp

def insert_noHOHO(text):
    result = ""
    for char in text:
        result += f"n{char}n{char}o{char}o{char}H{char}H{char}O{char}O"
    return result

font = Glyphs.font
if font:
    tab = font.currentTab
    if tab:
        original_text = tab.text
        new_text = insert_noHOHO(original_text)
        tab.text = new_text
    else:
        Message("No Edit tab open", "Please open an Edit tab to use this script.")
else:
    Message("No font open", "Please open a font to use this script.")