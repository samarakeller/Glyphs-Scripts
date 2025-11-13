# MenuTitle: AOCK – Adjust Overall Character Kerning
# -*- coding: utf-8 -*-
__doc__ = """
Adjusts kerning for both left and right groups of one or more glyphs
by a specified value, in the current master only.
"""

import GlyphsApp
from vanilla import FloatingWindow, EditText, TextBox, Button

font = Glyphs.font
master = font.selectedFontMaster


class KerningAdjusterUI:
    def __init__(self):
        self.w = FloatingWindow((300, 140), "Adjust Kerning Groups")

        self.w.text1 = TextBox((15, 15, -15, 20), "Glyph (e.g. A v ?):")
        self.w.glyphsInput = EditText((15, 35, -15, 22), placeholder="A o …")

        self.w.text2 = TextBox((15, 65, 140, 20), "Adjustment (e.g. 5):")
        self.w.valueInput = EditText((160, 65, 50, 22), text="0")

        self.w.runButton = Button((15, 100, -15, 25), "Apply Value", callback=self.applyAdjustment)

        self.w.open()

    def applyAdjustment(self, sender):
        glyphNames = self.w.glyphsInput.get().replace(",", " ").split()
        try:
            adjustment = float(self.w.valueInput.get())
        except ValueError:
            Glyphs.showNotification("Kerning Adjuster", "⚠️ Enter a valid number.")
            return

        totalCount = 0

        for glyphName in glyphNames:
            g = font.glyphs[glyphName]
            if not g:
                print(f"⚠️ Glyph '{glyphName}' not found.")
                continue

            leftGroup = f"@MMK_L_{g.leftKerningGroup or glyphName}"
            rightGroup = f"@MMK_R_{g.rightKerningGroup or glyphName}"

            kerningDict = font.kerning[master.id]
            count = 0

            for leftKey in kerningDict.keys():
                for rightKey in kerningDict[leftKey].keys():
                    if leftKey in (leftGroup, rightGroup) or rightKey in (leftGroup, rightGroup):
                        oldValue = kerningDict[leftKey][rightKey]
                        newValue = oldValue + adjustment
                        kerningDict[leftKey][rightKey] = newValue
                        count += 1

            if count:
                print(f"Adjusted {count} pairs for {glyphName} ({leftGroup}, {rightGroup}) by {adjustment}.")
            else:
                print(f"No kerning pairs found for {glyphName}.")
            totalCount += count

        if totalCount > 0:
            Glyphs.showNotification(
                "Kerning Adjusted",
                f"Adjusted {totalCount} pairs across {len(glyphNames)} glyphs by {adjustment} in {master.name}."
            )
            print(f"✅ Done! Adjusted {totalCount} kerning pairs in {master.name}.")
            self.w.close()
        else:
            Glyphs.showNotification(
                "No Kerning Changed",
                "No kerning pairs were found or adjusted. Window remains open."
            )
            print("⚠️ No kerning pairs done. Window remains open.")


KerningAdjusterUI()
