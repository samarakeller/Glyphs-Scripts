# MenuTitle: Samara's Glyph Race
# -*- coding: utf-8 -*-
# Glyph Timer with history of last 20 glyphs (per glyph name, not per master)
from vanilla import FloatingWindow, TextBox, Button
class Timer():
	def __init__(self):
		self.currentGlyph = Glyphs.font.selectedLayers[0].parent if Glyphs.font and Glyphs.font.selectedLayers else None
		self.start = time.time()
		
		# Keep track of work history (glyph names only, max 20)
		self.history = []
		
		# Floating window with text + reset button
		self.w = FloatingWindow((240, 400), "Glyph Race")
		self.w.text = TextBox((10, 10, -10, 40), "⏱ Start already…")
		self.w.summary = TextBox((10, 40, -10, -40), "")
		self.w.resetButton = Button((10, -30, -10, 20), "New Round", callback=self.resetAll)
		
		self.w.open()
		self.addCallbacks()
		self.w.bind('close', self.removeCallbacks)
	
	def addCallbacks(self):
		Glyphs.addCallback(self.updateInterface, UPDATEINTERFACE)
	
	def removeCallbacks(self, sender):
		Glyphs.removeCallback(self.updateInterface, UPDATEINTERFACE)
	
	def formatTime(self, seconds):
		"""Helper to format seconds into mm:ss"""
		m = int(seconds // 60)
		s = int(seconds % 60)
		return f"{m:02}:{s:02}"
	
	def updateInterface(self, sender):
		if not Glyphs.font or not Glyphs.font.selectedLayers:
			return
		
		newGlyph = Glyphs.font.selectedLayers[0].parent
		if self.currentGlyph != newGlyph:
			# switched glyph → store time
			timeElapsed = time.time() - self.start
			if self.currentGlyph:
				prev = self.currentGlyph.userData.get("timer", 0)
				self.currentGlyph.userData["timer"] = prev + timeElapsed
				
				# update history (keep last 20 unique glyphs, newest last)
				if self.currentGlyph.name in self.history:
					self.history.remove(self.currentGlyph.name)
				self.history.append(self.currentGlyph.name)
				if len(self.history) > 40:
					self.history.pop(0)
				
				print(f"{self.currentGlyph.name} ⏱ {self.formatTime(self.currentGlyph.userData['timer'])}")
			
			# reset timer
			self.start = time.time()
			self.currentGlyph = newGlyph
		
		# update live timer for current glyph
		if self.currentGlyph:
			total = self.currentGlyph.userData.get("timer", 0) + (time.time() - self.start)
			self.w.text.set(f"{self.currentGlyph.name} ⏱ {self.formatTime(total)}")
		
		# show history summary (last 20 glyphs)
		summaryLines = []
		for gName in reversed(self.history):
			g = Glyphs.font.glyphs[gName]
			if g:
				t = g.userData.get("timer", 0)
				if g == self.currentGlyph:
					t += time.time() - self.start
				summaryLines.append(f"{gName}: {self.formatTime(t)}")
		self.w.summary.set("\n".join(summaryLines))
	
	def resetAll(self, sender):
		"""Clear all timers in font"""
		if not Glyphs.font:
			return
		for g in Glyphs.font.glyphs:
			if "timer" in g.userData:
				del g.userData["timer"]
		print("🔄 All glyph timers reset.")
		self.w.text.set("⏱ Reset – Work Bitch!")
		self.w.summary.set("")
		self.history = []

Timer()
