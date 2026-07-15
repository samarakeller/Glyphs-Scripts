#MenuTitle: Copy components in all Masters
# -*- coding: utf-8 -*-
__doc__ = """
Kopiert alle Komponenten der ausgewählten Glyphe aus dem aktuellen Master
in alle anderen Master.
"""

from GlyphsApp import *

font = Glyphs.font

if not font:
    Message("Kein Font geöffnet.", "Fehler")
else:
    # Aktuell geöffneter Master (im Edit-View oder Font-Übersicht)
    currentMasterIndex = font.masterIndex
    currentMaster = font.masters[currentMasterIndex]

    # Ausgewählte Glyphen (funktioniert in der Font-Übersicht & Edit-View)
    selectedGlyphs = []

    # Font-Übersicht: font.selectedLayers
    if font.selectedLayers:
        for layer in font.selectedLayers:
            if layer.parent not in selectedGlyphs:
                selectedGlyphs.append(layer.parent)

    if not selectedGlyphs:
        Message("Bitte mindestens eine Glyphe auswählen.", "Keine Auswahl")
    else:
        report = []

        for glyph in selectedGlyphs:
            # Quell-Layer = aktueller Master
            sourceLayer = glyph.layers[currentMaster.id]

            if not sourceLayer:
                report.append(f"⚠️  {glyph.name}: Kein Layer für aktuellen Master gefunden.")
                continue

            sourceComponents = sourceLayer.components

            if not sourceComponents:
                report.append(f"⚠️  {glyph.name}: Keine Komponenten im aktuellen Master ({currentMaster.name}).")
                continue

            for master in font.masters:
                # Quell-Master überspringen
                if master.id == currentMaster.id:
                    continue

                targetLayer = glyph.layers[master.id]

                if not targetLayer:
                    report.append(f"⚠️  {glyph.name} → {master.name}: Kein Ziel-Layer gefunden.")
                    continue

                # Überspringen wenn bereits Komponenten vorhanden
                if targetLayer.components:
                    report.append(f"⏭️  {glyph.name} → {master.name}: Bereits Komponenten vorhanden, übersprungen.")
                    continue

                # Komponenten kopieren und in Ziel-Layer einfügen
                addedCount = 0
                for comp in sourceComponents:
                    newComp = comp.copy()
                    targetLayer.components.append(newComp)
                    addedCount += 1

                report.append(f"✅  {glyph.name} → {master.name}: {addedCount} Komponent(en) hinzugefügt.")

        # Zusammenfassung anzeigen
        summary = "\n".join(report)
        print(summary)
        Message(summary, "Komponenten kopiert")