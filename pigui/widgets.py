import pygame as pg
from collections import namedtuple
from pigui.colors import *
from pigui.events import *
import os

Offset = namedtuple("Offset", ["x", "y"])

def load_surf(img):
	if isinstance(img, pg.Surface):
		surf = img
	elif isinstance(img, tuple):
		surf = pg.image.load(os.path.join(*img)).convert()
	elif isinstance(img, str):
		surf = pg.image.load(img).convert()
	else:
		raise TypeError(f"img must be a tuple of strings representing a path to an image or a Pygame Surface not {img}")

	return surf

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
		self.alpha=alpha
		self.selected = False

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

'''NEEDED WIDGETS LIST

Container:
A container holds multiple widgets into itself. It can be thought of as a "box" containing other widgets.
They can sometimes be seen as menus as well although they are more abstract than them. Those can be organized in different ways.
- Tabs
- Menus
- Container


'''