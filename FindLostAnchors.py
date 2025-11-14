# MenuTitle: Find lost Anchors
# -*- coding: utf-8 -*-

from __future__ import print_function

__doc__ = """
Find base glyphs that contain anchors which are not referenced by any components or marks.
Opens a tab listing them and prints a detailed report in the macro window.
Ignores mark glyphs themselves.
Only checks one master layer per glyph to avoid duplicates.
"""

import GlyphsApp

font = Glyphs.font
if not font:
    Message("No Font Open", "Open a font and run again.")
    raise Exception("No font open")

print("🔍 Collecting anchor usage per base glyph…")

# Only consider non-mark (base) glyphs
baseGlyphs = [g for g in font.glyphs if g.category != "Mark"]

# Map base glyph name to set of anchors used by any components or marks
anchorUsagePerBase = {g.name: set() for g in baseGlyphs}

# 1. Check components: if a component references a base, the anchor used counts for that base
for g in baseGlyphs:
    l = g.layers[0]  # only check first master layer
    for comp in l.components:
        baseName = comp.componentName
        if baseName in anchorUsagePerBase and comp.anchor:
            anchorUsagePerBase[baseName].add(comp.anchor)

# 2. Check mark attachments: a mark uses its _xxx anchors on base glyphs
for g in font.glyphs:
    if g.category == "Mark":
        l = g.layers[0]  # only check first master layer
        for a in l.anchors:
            baseAnchorName = a.name[1:] if a.name.startswith("_") else a.name
            for baseGlyph in baseGlyphs:
                if baseAnchorName in [b.name for b in baseGlyph.layers[0].anchors]:
                    anchorUsagePerBase[baseGlyph.name].add(baseAnchorName)

# 3. Determine truly unused anchors per base glyph
unusedAnchorsPerGlyph = {}
for g in baseGlyphs:
    l = g.layers[0]  # only check first master layer
    unused = [a.name for a in l.anchors if a.name not in anchorUsagePerBase[g.name]]
    if unused:
        unusedAnchorsPerGlyph[g.name] = sorted(set(unused))  # dedupe

# 4. Print report
Glyphs.clearLog()
if not unusedAnchorsPerGlyph:
    Message("All Good!", "No unused anchors found in base glyphs.")
    print("No unused anchors found in base glyphs.")
    raise SystemExit

print("🔹 Unused Anchor Report (base glyphs only):\n")
for gName in sorted(unusedAnchorsPerGlyph.keys()):
    print(f"{gName}: {', '.join(unusedAnchorsPerGlyph[gName])}")

# 5. Open tab with affected base glyphs
tab = font.newTab()
tab.layers = [font.glyphs[gName].layers[0] for gName in sorted(unusedAnchorsPerGlyph.keys())]
print("\nOpened tab with base glyphs containing unused anchors.")
