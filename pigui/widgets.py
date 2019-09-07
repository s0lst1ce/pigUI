import pygame as pg
from pygame import freetype
from collections import namedtuple
from pigui.colors import *
from pigui.events import *
import os

Offset = namedtuple("Offset", ["x", "y"])

class Widget(object):
	"""An abstract class from which most widgets inherit. Must always belong to a Container.
	w:     width of the widget
	h:     height of the widget
	surf:  surface to pass to the widget. This will be overriden if special methods build their own surfaces
	img:   image file to be laoded from disk. This argument must be a tuple of strings specifying the relative path to the asset.
	alpha: whether the widget must provide support for the alpha channel. If True the given surface (if any) will be converted to alpha. Likewise it will be converted to RGB profile otherwise for improved performance.

	If both surf and img arguments are provided then the class will give an error upon creation."""
	def __init__(self, w, h, *args, surf=None, img=None, alpha=True, **kwargs):
		self.w = w
		self.h = h
		self.hover = False
		self.hovered = False

		#making surface
		assert surf==None or img==None, ValueError(f"Both surf ({surf}) and img ({img}) were provided.")
		if surf:
			self.surf = surf
		elif img:
			self.surf = self.load_img(img)

		self.changed = True #whether the surface has changed since the last time the container read it.


	def load_img(self, path):
		"""return a surface representing the image located at the specified "path" location. The surface will be of the appropriate profile (RGB or RGBA)"""
		surf = pg.image.load(os.path.join(*path))

		if self.alpha:
			return surf.convert_alpha()
		else:
			return surf.convert()


	def update(self, *args):
		"""generic update function. All widgets should have one since containers will expect one."""
		pass


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
					raise TypeError(f"A background, bgcolor, or alpha must be set")
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
			if isinstance(background, pg.Surface):
				surf = background
			elif isinstance(background, tuple):
				surf = pg.image.load(os.path.join(*background)).convert()
			elif isinstance(background, str):
				surf = pg.image.load(background).convert()
			self.bgsurf = pg.transform.scale(surf, (w, h))
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
		if isinstance(background, pg.Surface):
			surf = background
		elif isinstance(background, tuple):
			surf = pg.image.load(os.path.join(*background)).convert()
		elif isinstance(background, str):
			surf = pg.image.load(background).convert()
		else:
			raise TypeError(f"background must be a tuple of strings representing a path to an image or a Pygame Surface not {background}")

		rect = surf.get_rect()
		return cls(rect.w, rect.h, *args, background=background, **kwargs)

	@classmethod
	def from_text(cls, text, *args, offset=None, **kwargs):
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

class AbstractButton(Widget):
	"""docstring for Button"""
	def __init__(self, w, h, *args, alpha=False, action=None, locked=False, **kwargs):
		super().__init__(w, h, *args, alpha=alpha, **kwargs)
		self.w = w
		self.h = h
		self.action = action
		self.events = [pg.MOUSEBUTTONUP]
		self._locked = locked
		self.hover = True
		self.i = 0

	@property
	def locked(self):
		return self._locked

	def update(self):
		if self.hovered and not self._locked:
			global PYGUI_DISPATCHER
			events = PYGUI_DISPATCHER[self]
			if events:
				self.action()


class TextButton(AbstractButton, Label):
	"""a button with text"""
	def __init__(self, w, h, alpha=False, action=None, text="", bgcolor=None, fgcolor=BLACK, font=None, font_size=20, underlined=False, bold=False, highlight_color=None, lock_color=LIGHT_GREY):
		super().__init__(w, h, alpha=alpha, action=action, text=text, bgcolor=bgcolor, fgcolor=fgcolor, font=font, font_size=font_size, underlined=underlined, bold=bold)
		self.highlighted = False
		self.hover = True
		self.lock_color=lock_color

		#guessing highlight color
		if not highlight_color:
			self.highlight_color = (fgcolor[0]-(0.3*fgcolor[0]), fgcolor[1]-(0.3*fgcolor[1]), fgcolor[2]-(0.3*fgcolor[2]), fgcolor[3])
		else:
			self.highlight_color = highlight_color

	def __repr__(self):
		return f"<TextButton({self.w}, {self.h}), text={self._text}, hovered={self.hovered}"

	@property
	def locked(self):
		return self.AbstractButton.locked()

	@locked.setter
	def locked(self, value):
		if self._locked == bool(value):
			return

		self.font.fgcolor = bool(value)
		self.changed=True
		self.make_surf()


	def update(self):
		super().update()
		if self._locked:
			return

		if not self.hovered:
			if self.highlighted:
				self.highlighted = False
				self.font.fgcolor = self.fgcolor
				self.changed = True
				self.make_surf()
		else:
			if self.highlighted:
				return
			self.highlighted = True
			self.font.fgcolor = self.highlight_color
			self.changed = True
			self.make_surf()






'''NEEDED WIDGETS LIST
- Label
- Input
- Buttons
	- ImageButton
	- TextButton

Container:
A container holds multiple widgets into itself. It can be thought of as a "box" containing other widgets.
They can sometimes be seen as menus as well although they are more abstract than them. Those can be organized in different ways.
- Tabs
- Menus
- Container


'''