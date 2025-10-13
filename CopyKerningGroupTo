# MenuTitle: Copy Kerning Group to
# -*- coding: utf-8 -*-
from GlyphsApp import *
from vanilla import *

class CopyKerningGroupWindow(object):
    def __init__(self):
        self.w = Window((400, 180), "Copy Kerning Group to")
        self.w.instructions = TextBox(
            (15, 10, -15, 40),
            "Enter kerning groups to copy:\nExample: A = AE"
        )
        self.w.groupPairs = TextEditor((15, 55, -15, 80))
        self.w.copyButton = Button((-110, -40, 90, 30), "Copy", callback=self.copyKerningGroups)
        self.w.open()

    def resolveKey(self, font, key):
        """Return readable name or group name for kerning key (string or UUID)."""
        if isinstance(key, str):
            # It's either a group (@MMK_L_ or @MMK_R_) or glyph name
            return key
        # Otherwise, assume it's a UUID (Glyphs 3)
        g = font.glyphForId_(key)
        return g.name if g else None

    def copyKerningGroups(self, sender):
        font = Glyphs.font
        if not font:
            Message("No font open", "Please open a font in Glyphs.")
            return

        lines = self.w.groupPairs.get().splitlines()
        pairs = []
        for line in lines:
            if "=" in line:
                base, target = [s.strip() for s in line.split("=", 1)]
                if base and target:
                    pairs.append((base, target))

        if not pairs:
            Message("No pairs", "Please enter at least one pair in the format A=AE.")
            return

        successfulPairs = 0

        for base, target in pairs:
            leftSource = f"@MMK_L_{base}"
            leftTarget = f"@MMK_L_{target}"
            rightSource = f"@MMK_R_{base}"
            rightTarget = f"@MMK_R_{target}"

            for master in font.masters:
                kerningDict = font.kerning[master.id]

                # --- LEFT SIDE COPY ---
                if leftSource in kerningDict:
                    for rightKey, value in kerningDict[leftSource].items():
                        rightName = self.resolveKey(font, rightKey)
                        if not rightName:
                            continue
                        try:
                            font.setKerningForPair(master.id, leftTarget, rightName, value)
                            successfulPairs += 1
                        except Exception as e:
                            print(f"Error copying {leftSource} → {leftTarget} ({rightName}): {e}")
                else:
                    print(f"⚠️ No left kerning found for {leftSource} in master {master.name}")

                # --- RIGHT SIDE COPY ---
                for leftKey, rightDict in kerningDict.items():
                    leftName = self.resolveKey(font, leftKey)
                    if not leftName or rightSource not in rightDict:
                        continue
                    value = rightDict[rightSource]
                    try:
                        font.setKerningForPair(master.id, leftName, rightTarget, value)
                        successfulPairs += 1
                    except Exception as e:
                        print(f"Error copying {rightSource} → {rightTarget} ({leftName}): {e}")

        if successfulPairs > 0:
            Message("Kerning copied!", f"Successfully copied {successfulPairs} kerning pairs.")
        else:
            Message("No kerning found", "No kerning pairs found for the specified groups.")

        self.w.close()


CopyKerningGroupWindow()
