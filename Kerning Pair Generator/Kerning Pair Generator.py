# MenuTitle: Kerning Pairs Generator
# -*- coding: utf-8 -*-
from GlyphsApp import Glyphs, Message
import vanilla

# Mapping for ambiguous characters → glyph names
CHAR_TO_GLYPHNAME = {
    # numbers
    "0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
    "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine",
    # punctuation & symbols
    ".": "period",
    ",": "comma",
    ":": "colon",
    ";": "semicolon",
    "!": "exclam",
    "?": "question",
    "-": "hyphen",
    "_": "underscore",
    "/": "slash",
    "\\": "backslash",
    "#": "numbersign",
    "~": "tilde",
    "°": "degree",
    "'": "quotesingle",
    "\"": "quotedbl",
    "*": "asterisk",
    "@": "at",
}

# Predefined sets in UI (user-friendly characters)
PREDEFINED_SETS = {
    "lowercase": list("abcdefghijklmnopqrstuvwxyz"),
    "uppercase": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    "numbers": list("0123456789"),
    "punctuation": [".", ",", ":", ";", "!", "?", "-", "_", "/", "\\",
                    "#", "~", "°", "'", "\"", "*", "@"],
}


def normalizeInput(tokens, font):
    """
    Convert characters or glyph names into valid glyph names.
    Uses manual CHAR_TO_GLYPHNAME, Unicode lookup in font, Glyphs niceGlyphName,
    or skips missing.
    """
    result = []
    skipped = []
    for t in tokens:
        # First: manual mapping
        if t in CHAR_TO_GLYPHNAME:
            glyphName = CHAR_TO_GLYPHNAME[t]
            if font.glyphs[glyphName]:
                result.append(glyphName)
            else:
                skipped.append(t)
            continue

        # Second: single character → Unicode lookup
        if len(t) == 1:
            uni = ord(t)
            hexUni = f"{uni:04X}"
            glyph = None
            try:
                glyph = font.glyphForUnicode_(hexUni)  # Glyphs 3 API
            except:
                glyph = None

            if not glyph:
                # fallback: Glyphs niceGlyphName (maps Unicode → name like "aacute")
                glyphName = Glyphs.niceGlyphName(hexUni)
                if glyphName and font.glyphs[glyphName]:
                    glyph = font.glyphs[glyphName]

            if not glyph:
                # fallback: search manually
                for g in font.glyphs:
                    if g.unicode == hexUni:
                        glyph = g
                        break

            if glyph:
                result.append(glyph.name)
                continue
            else:
                skipped.append(t)
                continue

        # Third: user typed a glyph name directly
        if font.glyphs[t]:
            result.append(t)
        else:
            skipped.append(t)

    return result, skipped


class KerningPairsGenerator(object):
    def __init__(self):
        self.w = vanilla.FloatingWindow((360, 240), "Kerning Pairs Generator")

        # First set
        self.w.text1 = vanilla.TextBox((10, 10, -10, 20), "First set:")
        self.w.firstSet = vanilla.EditText((10, 30, -130, 22), placeholder="A")
        self.w.firstDropdown = vanilla.PopUpButton(
            (-120, 30, -10, 22),
            ["(none)"] + list(PREDEFINED_SETS.keys()),
            callback=self.fillFirstSet,
        )

        # Second set
        self.w.text2 = vanilla.TextBox((10, 65, -10, 20), "Second set:")
        self.w.secondSet = vanilla.EditText((10, 85, -130, 22), placeholder="B")
        self.w.secondDropdown = vanilla.PopUpButton(
            (-120, 85, -10, 22),
            ["(none)"] + list(PREDEFINED_SETS.keys()),
            callback=self.fillSecondSet,
        )

        # Pattern style
        self.w.patternText = vanilla.TextBox((10, 120, -10, 20), "Pattern:")
        self.w.patternChoice = vanilla.RadioGroup(
            (10, 140, -10, 40),
            ["AB (first-second)", "ABA (first-second-first)"],
            isVertical=True,
        )
        self.w.patternChoice.set(1)  # default = ABA

        # Generate button
        self.w.button = vanilla.Button((10, 190, -10, 30), "Generate", callback=self.generate)

        self.w.open()
        self.w.makeKey()

    def fillFirstSet(self, sender):
        choice = sender.get()
        if choice > 0:
            key = list(PREDEFINED_SETS.keys())[choice - 1]
            self.w.firstSet.set(" ".join(PREDEFINED_SETS[key]))

    def fillSecondSet(self, sender):
        choice = sender.get()
        if choice > 0:
            key = list(PREDEFINED_SETS.keys())[choice - 1]
            self.w.secondSet.set(" ".join(PREDEFINED_SETS[key]))

    def generate(self, sender):
        font = Glyphs.font
        if not font:
            Message("No font open", "Open a font to generate pairs.")
            return

        firstInput, skipped1 = normalizeInput(self.w.firstSet.get().strip().split(), font)
        secondInput, skipped2 = normalizeInput(self.w.secondSet.get().strip().split(), font)

        skipped = skipped1 + skipped2
        if skipped:
            msg = "Skipped inputs (not found in font): " + ", ".join(skipped)
            print("⚠️", msg)
            Message("Some glyphs skipped", msg)

        if not firstInput or not secondInput:
            Message("Empty input", "Fill in both sets to generate pairs.")
            return

        pairs = []
        pattern = self.w.patternChoice.get()
        for f in firstInput:
            for s in secondInput:
                if pattern == 0:  # AB
                    seq = f"/{f}/{s}"
                else:  # ABA
                    seq = f"/{f}/{s}/{f}"
                pairs.append(seq)

        tabString = " ".join(pairs)
        font.newTab(tabString)


KerningPairsGenerator()
