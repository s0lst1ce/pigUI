import pygame as pg
from pigui.widgets import *
from pigui.colors import *
from pigui.labels import Label
from pigui.events import *

class InputField(Widget):
	"""docstring for InputField, a Widget in which you can write text. It is recommended to use the max_chars parameter for performance"""
	def __init__(self, w, h, alpha=False, hint_text="Type here...", fgcolor=BLACK, bgcolor=None, font=None, font_size=20, underlined=False, bold=False, max_chars=None, max_width=None, offset=None):
		super().__init__(w, h, alpha=alpha)
		self.hint_text = hint_text
		self.fgcolor = fgcolor
		self.bgcolor = bgcolor
		self.underlined = underlined
		self.bold = bold
		self.font_size = font_size
		self.font = font
		self.max_width = max_width
		self.max_chars = max_chars

		#events
		self.events = [pg.KEYDOWN, pg.MOUSEBUTTONDOWN]
		self.hover = True

		#text
		if not self.hint_text:
			self.hint_text = " "
		if self.max_chars:
			assert len(self.hint_text)<=self.max_chars, ValueError(f"Hint text ({len(self.hint_text)} chars) is larger than maximum character count ({len(self.max_chars)} chars)")
		self.text = self.hint_text

		if not self.max_width:
			self.max_width = w

		#displayer; the amont of kwags is quite high which clogs __init__. Should the dunder method use less redundant kwrgs and accept a **kwarg instead which would be passed to the displayer?
		self.displayer = Label(self.w, self.h, alpha=alpha, text=hint_text, fgcolor=fgcolor, bgcolor=bgcolor, font=font, font_size=font_size, underlined=underlined, bold=bold, offset=offset)

	@property
	def surf(self):
		return self.displayer.surf

	@surf.setter
	def surf(self, val):
		self.displayer.surf = val
		self.displayer.changed = True
		self.changed =True	


	def shown_text(self):
		if self.max_chars:
			return self.text[:-self.max_chars]
		else:
			full_w = self.displayer.font.get_rect(self.text).w
			if full_w<=self.max_width:
				return self.text

			approx_char_size = full_w/len(self.text)
			shown_chars = int(self.w/approx_char_size)+1
			while full_w>self.w:
				print(shown_chars, self.text[shown_chars:])
				shown_chars-=1
				full_w = self.displayer.font.get_rect(self.text[len(self.text)-shown_chars:]).w
			return self.text[len(self.text)-shown_chars:]

	def update(self):
		events=None
		if self.hovered:
			events = Dispatcher()[self]
			for e in events:
				if e.type==pg.MOUSEBUTTONDOWN:
					global SELECTED
					SELECTED = self

		if SELECTED==self:
			if not events:
				events = Dispatcher()[self]
			for e in events:
				if e.type==pg.KEYDOWN:
					if e.key==8:
						if len(self.text)<=1 or self.text==self.hint_text:
							self.text = self.hint_text
						else:
							self.text = self.text[:-1]
					else:
						if self.text!=self.hint_text:
							self.text+=e.unicode
						else:
							self.text = e.unicode

					self.displayer.text = self.shown_text()
					self.displayer.changed = True
					self.changed = True
					print(self.text, self.shown_text())
