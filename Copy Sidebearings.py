# MenuTitle: Copy Sidebearings
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Alex Jacque <alexjacque.com> and Mekkablue > Steal Metrics
# Adapted for personal use by Samara Keller

from __future__ import division, print_function, unicode_literals
__doc__ = """
Copy sidebearings from one font to another.
"""

import vanilla
import traceback
from GlyphsApp import Glyphs

class CopySidebearings(object):
    """GUI for copying glyph sidebearings from one font to another"""
    
    def __init__(self):
        # Check if we have at least 2 fonts open
        if len(Glyphs.fonts) < 2:
            Glyphs.showMacroWindow()
            print("Requires two fonts to be open.")
            return
        
        # Get list of open fonts
        self.fonts = list(Glyphs.fonts)
        fontNames = [f"{i + 1}: {font.familyName}" for i, font in enumerate(self.fonts)]
        
        # Window 'self.w':
        windowWidth = 200
        windowHeight = 260
        self.w = vanilla.FloatingWindow(
            (windowWidth, windowHeight),  # default window size
            "Copy Sidebearings",  # window title
            minSize=(windowWidth, windowHeight + 19),  # minimum size (for resizing)
            maxSize=(windowWidth, windowHeight + 19),  # maximum size (for resizing)
        )

        # UI elements:
        linePos, inset, lineHeight = 15, 15, 25

        # Source font dropdown
        self.w.sourceUFOText = vanilla.TextBox((inset, linePos, 90, 22), "Source Font:", sizeStyle="small")
        self.w.sourceUFODropDown = vanilla.PopUpButton((inset, linePos + 20, -inset, 20), fontNames)
        self.w.sourceUFODropDown.set(0)
        linePos += 50

        # Destination font dropdown
        self.w.destinationUFOText = vanilla.TextBox((inset, linePos, 90, 22), "Destination Font:", sizeStyle="small")
        self.w.destinationUFODropDown = vanilla.PopUpButton((inset, linePos + 20, -inset, 20), fontNames)
        if len(fontNames) > 1:
            self.w.destinationUFODropDown.set(1)
        linePos += 50

        # Divider
        self.w.divider1 = vanilla.HorizontalLine((inset, linePos, -inset, 1))
        linePos += 15

        # Glyphs scope area
        self.w.glyphsRadioGroup = vanilla.RadioGroup((inset, linePos, -inset, 50), ["All Glyphs", "Selected Glyphs"], sizeStyle="small")
        self.w.glyphsRadioGroup.set(0)  # default to all glyphs
        linePos += 60

        # Divider
        self.w.divider2 = vanilla.HorizontalLine((inset, linePos, -inset, 1))
        linePos += 15

        # Commit button
        self.w.commitButton = vanilla.Button((inset, linePos, -inset, 20), "Copy Sidebearings", sizeStyle="small", callback=self.copySidebearings)
        linePos += 30

        # Note
        self.w.note = vanilla.TextBox((inset, linePos, -inset, 15), "Open output window for results.", sizeStyle="mini", alignment="center")

        self.w.open()  # go go gadget window
        self.w.makeKey()

    def copySidebearings(self, sender):
        try:
            sourceFont = self.fonts[self.w.sourceUFODropDown.get()]
            destinationFont = self.fonts[self.w.destinationUFODropDown.get()]
            
            sourceGlyphsCopied = []  # glyphs with successfully copied side bearings
            sourceGlyphsNotInDestination = []  # glyphs from source not in destination font
            destGlyphsNotInSource = []  # glyphs in destination not contained in source
            
            copyAll = (self.w.glyphsRadioGroup.get() == 0)
            
            # Get scope
            if copyAll:
                glyphs = sourceFont.glyphs  # all glyphs
            else:
                # Get selected glyphs from current font view
                currentFont = Glyphs.font
                if currentFont is None:
                    Glyphs.showMacroWindow()
                    print("Please select at least one glyph in the source font from which to copy the sidebearings.")
                    return
                
                selectedLayers = currentFont.selectedLayers
                if not selectedLayers:
                    Glyphs.showMacroWindow()
                    print("Please select at least one glyph in the source font from which to copy the sidebearings.")
                    return
                
                glyphs = [layer.parent for layer in selectedLayers if layer.parent in sourceFont.glyphs]
                if not glyphs:
                    Glyphs.showMacroWindow()
                    print("No selected glyphs found in the source font.")
                    return
            
            # Copy sidebearings
            for glyph in glyphs:
                if glyph.name in destinationFont.glyphs:
                    destGlyph = destinationFont.glyphs[glyph.name]
                    
                    # Begin undo group
                    destinationFont.disableUpdateInterface()
                    
                    try:
                        # For empty glyphs, copy width only
                        if not glyph.layers[0].paths:  # no contours
                            destGlyph.layers[0].width = glyph.layers[0].width
                        else:
                            # Copy left and right margins (sidebearings)
                            destGlyph.layers[0].LSB = glyph.layers[0].LSB  # Left Side Bearing
                            destGlyph.layers[0].RSB = glyph.layers[0].RSB  # Right Side Bearing
                        
                        sourceGlyphsCopied.append(glyph.name)
                        
                    except Exception as e:
                        print(f"Error copying {glyph.name}: {e}")
                    finally:
                        destinationFont.enableUpdateInterface()
                        
                else:
                    sourceGlyphsNotInDestination.append(glyph.name)
            
            # Check for glyphs in destination not in source (only when copying all)
            if copyAll:
                for glyph in destinationFont.glyphs:
                    if glyph.name not in sourceFont.glyphs:
                        destGlyphsNotInSource.append(glyph.name)
            
            # Sort results
            sourceGlyphsCopied.sort()
            sourceGlyphsNotInDestination.sort()
            destGlyphsNotInSource.sort()
            
            # Show macro window and print results
            Glyphs.showMacroWindow()
            print("### Source Glyph Sidebearings Successfully Copied ###")
            for glyphName in sourceGlyphsCopied:
                print(glyphName)
            print("")
            
            print("### Source Glyphs NOT in Destination (skipped) ###")
            for glyphName in sourceGlyphsNotInDestination:
                print(glyphName)
            print("")
            
            if copyAll:
                print("### Glyphs in Destination NOT in Source (missed) ###")
                for glyphName in destGlyphsNotInSource:
                    print(glyphName)
                print("")
            
            # Close dialog
            self.w.close()
            
            # Show completion message
            Glyphs.showMacroWindow()
            print(f"Copy completed!\nCopied: {len(sourceGlyphsCopied)} glyphs\nSkipped: {len(sourceGlyphsNotInDestination)} glyphs")
            
        except Exception as e:
            Glyphs.showMacroWindow()
            print(f"Error: {e}")
            print(traceback.format_exc())

# Run the script
CopySidebearings()
