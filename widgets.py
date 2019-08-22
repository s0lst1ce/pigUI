import pygame as pg
from pygame import freetype
from colors import *
import os

class Widget(object):
	"""An abstract class from which most widgets inherit. Must always belong to a Container.
	w:     width of the widget
	h:     height of the widget
	surf:  surface to pass to the widget. This will be overriden if special methods build their own surfaces
	img:   image file to be laoded from disk. This argument must be a tuple of strings specifying the relative path to the asset.
	alpha: whether the widget must provide support for the alpha channel. If True the given surface (if any) will be converted to alpha. Likewise it will be converted to RGB profile otherwise for improved performance.

	If both surf and img arguments are provided then the class will give an error upon creation."""
	def __init__(self, w, h, surf=None, img=None, alpha=True, can_hover=False):
		self.w = w
		self.h = h
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
	underlined: whether the text should be underlined. This is a software rendering post-processing.
	bold:       whether the text should be bold. Note that this is a software rendering post-processing done on the font. Prefer bold fonts instead"""
	def __init__(self, w, h, alpha=False, text="", bgcolor=None, fgcolor=BLACK, font=None, font_size=20, underlined=False, bold=False, can_hover=False, max_chars=False):
		super(Label, self).__init__(w, h, alpha=alpha, can_hover=can_hover)

		#text properties
		self._text = text
		self.bgcolor = bgcolor
		if bgcolor==None:
			if alpha:
				self.bgcolor = ALPHA
			else:
				self.bgcolor = WHITE
		else:
			self.bgcolor = bgcolor
		self.fgcolor = fgcolor
		self.bold = bold
		self.underlined = underlined

		#font
		self.font = freetype.Font(font, font_size) #None means pg default
		self.font.underline = underlined
		self.font.strong = bold
		self.font.fgcolor = self.fgcolor

		#surface
		self.surf = pg.Surface((w, h))
		if alpha:
			self.surf = self.surf.convert_alpha()
		else:
			self.surf = self.surf.convert()
		self.surf.fill(self.bgcolor)

		#rendering text TODO: implement font scaling to fit text into provided surface
		nrect = self.font.get_rect(self._text)
		if nrect.w>self.w or nrect.h>self.h:
			raise ValueError("Text size larger than widget")
		self.render_text()

	def __repr__(self):
		return f'''<Label({self.w}, {self.h}), text="{self._text}"'''


	@property
	def text(self):
		return self._text

	@text.setter
	def text(self, string):
		nrect = self.font.get_rect(string)
		if nrect.w>self.w or nrect.h>self.h:
			raise ValueError("Text size larger than widget")
		self.changed = True
		self._text = string
		self.render_text()

	def render_text(self):
		self.surf.fill(self.bgcolor)
		rect = self.font.get_rect(self._text)
		x_offset = (self.w-rect.w)/2
		y_offset = (self.h-rect.h)/2
		if self.changed:
			self.font.render_to(self.surf, (x_offset, y_offset), text=self._text)


class AbstractButton(Widget):
	"""docstring for BUtton"""
	def __init__(self, w, h, alpha=False, action=None):
		self.w = w
		self.h = h
		self.action = action
		self.events = [pg.MOUSEBUTTONUP]
		
	def update(self):
		super(AbstractButton, self).update()
		if self.hovered:
			global PYGUI_DISPATCHER
			events = PYGUI_DISPATCHER[self]
			if events:
				self.action()


class TextButton(Label, AbstractButton):
	"""a button with text"""
	def __init__(self, w, h, alpha=False, action=None, text="", bgcolor=None, fgcolor=BLACK, font=None, font_size=20, underlined=False, bold=False, can_hover=False, max_chars=False):
		super(TextButton, self).__init__(w, h, alpha=False, action=None, text="Works", bgcolor=None, fgcolor=BLACK, font=None, font_size=20, underlined=False, bold=False, can_hover=False, max_chars=False)




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