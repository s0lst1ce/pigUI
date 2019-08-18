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

		self.changed = False #whether the surface has changed since the last time the container read it.


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


class Container(object):
	"""Container class

	x:       horizontal position used for drawing
	y:       vertical position used for drawing
	w:       width of the container
	h:       height of the container
	bgcolor: the background color of the widet. Transparent of None. This will slow things down.
	visible: whether the container's surface should be blitter to the screen"""
	def __init__(self, x, y, w, h, bgcolor=None, visible=True):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.bgcolor = bgcolor
		self.visible = visible
		
		self.widgets = {}
		self.surf = None


	def add(self, widget, x, y, w=None, h=None, fit=False, override=False):
		"""adds the specified widget to the ones handled by the container. \
		x: horizontal position of the widget in the container
		y: vertical position of the widget in the container
		w: how much of the width of the container the widget should use"""
		pass




	def remove(self, widget):
		pass


	def draw(self, dest, *args, **kwargs):
		"""this will draw the container and all it's widget to the dest surface in the specified location.
		Arguments can be a Rect instance or x, y, w, h integers. If no argument is provided then the container's attributes will be used."""
		if len(args)==0 and len(kwargs)==0:
			dest.blit(self.surf, self.x, self.y)
			return

		elif len(args)==1 and isinstance(args[0], pg.Rect):
			rect = args[0]
			if rect.w!=self.w or rect.h!=self.h:
				resized_surf = pg.transform.scale(self.surf, (rect.w, rect.h))
				dest.blit(resized_surf, (rect.x, rect.y))
				return

			dest.blit(self.surf, (rect.x, rect.y))
			return

		else:
			if "w" in kwargs or "h" in kwargs:
				resized_surf = pg.transform.scale(self.surf, (kwargs["w"], kwargs["h"]))
				dest.blit(resized_surf, (rect.x, rect.y))
				return
			dest.blit(self.surf, (args[0], args[1]))


	def get_rect(self):
		return pg.Rect(self.x, self.y, self.w, self.h)

	def get_surf(self):
		"""returns a copy of the container's surface"""
		return self.surf.copy()






class TextWidget(Widget):
	"""TextWidget is a class which provides methods for some common actions used by classes which render text.
	See Widget for the 4 first arguments.

	text:       string representing the text to be rendered
	bccolor:    background color
	fgcolor:    color of the text
	font:       font to be used. None will default to Pygame's default font
	underlined: whether the text should be underlined. This is a software rendering post-processing.
	bold:       whether the text should be bold. Note that this is a software rendering post-processing done on the font. Prefer bold fonts instead."""
	def __init__(self,w, h, surf=None, alpha=False, text="", bgcolor=None, fgcolor=BLACK, font=None, underlined=False, bold=False, can_hover=False):
		super(TextWidget, self, w, h, surf=surf, alpha=alpha, can_hover=can_hover).__init__()

		#text properties
		self.text = text
		self.font = font #None means pg default
		self.bgcolor = bgcolor
		self.fgcolor = fgcolor
		self.bold = bold
		self.underlined = underlined




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