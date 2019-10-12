import pygame as pg
from pygame import freetype
from pigui.widgets import *
from pigui.colors import *

class Label(Widget):
	"""Label is a class which provides methods for some common actions used by classes which render text.
	See Widget for the 4 first arguments.

	text:       string representing the text to be rendered
	bccolor:    background color
	fgcolor:    color of the text
	font:       font to be used. None will default to Pygame's default font
	font_size:  the size of the fonts in font points. Overriden by enlarge and offset
	underlined: whether the text should be underlined. This is a software rendering post-processing.
	bold:       whether the text should be bold. Note that this is a software rendering post-processing done on the font. Prefer bold fonts instead
	background: a surface or path to image to be used as background. Path may be a string or tuple of strings
	enlarge:        whether the rendered text should be fitted to the widget's surface. Can be overriden by offset
	offset:     tuple representing x and y offsets. If the rendered text is too big to respect the offsets then it will be resized. Works with enlarge."""
	def __init__(self, w, h, *args, alpha=False, text="", bgcolor=None, fgcolor=BLACK, font=None, font_size=20, underlined=False, bold=False, background=None, enlarge=True, offset=None, **kwargs):
		super().__init__(w, h, alpha=alpha)
		#making sure arguments are valid
		if bgcolor==None:
			if background==None:
				if alpha==None:
					raise ValueError(f"A background, bgcolor, or alpha must be set")
		else:
			if background:
				raise ValueError(f"Can't set background and bgcolor")

		self.enlarge = enlarge
		self.offset = offset
		self.background = background

		#text properties
		self._text = text
		self.fgcolor = fgcolor
		self.bold = bold
		self.underlined = underlined

		#font
		self.font = freetype.Font(font, font_size) #None means pg default
		self.font.underline = underlined
		self.font.strong = bold
		self.font.fgcolor = self.fgcolor

		#surface
		if background:
			self.bgsurf = pg.transform.scale(load_surf(background), (w, h))
		else:
			if bgcolor:
				self.bgcolor = bgcolor
			else:
				if alpha:
					self.bgcolor = ALPHA
				else:
					self.bgcolor = WHITE

			self.bgsurf = pg.Surface((w, h))
			self.bgsurf.fill(self.bgcolor)
		self.surf = self.bgsurf.copy()

		#evaluating offset
		if offset:
			if isinstance(offset, tuple):
				font_offset = Offset(*offset)
			elif isinstance(offset, Offset):
				font_offset = offset
			else:
				raise TypeError(f"offset must of type tuple(int, int) not {type(offset)}")

		#resizing font
		needs_rescale = False
		trect = self.font.get_rect(text)
		srect = self.chg_area = self.surf.get_rect()
		
		if offset: #applying offset
			srect.w -= font_offset.x*2
			srect.h -= font_offset.y*2

		if trect.w>srect.w or trect.h>srect.h:
			needs_rescale = True
		if needs_rescale or enlarge:
			ratios = (srect.w/trect.w, srect.h/trect.h)
			scale = min(ratios)
			self.font.size *= scale

		self.make_surf()

	def __repr__(self):
		return f'''<Label({self.w}, {self.h}), text="{self._text}"'''

	@classmethod
	def from_background(cls, background, *args, **kwargs):
		surf = load_surf(background)
		rect = surf.get_rect()
		return cls(rect.w, rect.h, *args, background=background, **kwargs)

	@classmethod
	def from_text(cls, text, *args, offset=None, font=None, **kwargs):
		pass

	@property
	def text(self):
		return self._text

	@text.setter
	def text(self, string):
		nrect = self.font.get_rect(string)
		if nrect.w>self.w or nrect.h>self.h:
			raise ValueError("Text size larger than widget")
		self.changed = True
		old_text = self._text
		self._text = string
		self.make_surf(old_text=old_text)

	def render_text(self):
		rendered = self.font.render(self._text)
		return rendered[0]

	def make_surf(self, old_text=None):
		if not self.changed:
			return

		#blitting background surface back on the main surface. -> fixes overlapping characters
		if not old_text:
			self.surf.blit(self.bgsurf, (0, 0))
		else:
			if self.font.get_rect(old_text)>self.font.get_rect(self._text):
				self.surf = self.bgsurf.copy()
			self.chg_area = self.surf.blit(self.bgsurf, (0,0), area=self.chg_area)

		offset = self.text_offsets(self._text)
		self.surf.blit(self.render_text(), (offset.x, offset.y))

	def text_offsets(self, text):
		rect = self.font.get_rect(text)
		x_offset = (self.w-rect.w)/2
		y_offset = (self.h-rect.h)/2
		return(Offset(x_offset, y_offset))
