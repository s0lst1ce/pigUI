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
		if bgcolor:
			self.bgcolor = bgcolor
		else:
			self.bgcolor = ALPHA
		self.visible = visible
		
		self.widgets = {}
		#an entry looks as such
		#Button: [resized_surf, area_rect, needs_resize, hover]
		#Widget: [Surface, Rect, Bool, Bool]
		self.hovered = [] #lsit of rect, widget tuples

		#surface
		self.surf = pg.Surface((w, h))
		self.surf.fill(self.bgcolor)


	def add(self, widget, x, y, w=None, h=None, fit=False, override=False, hover=False):
		"""adds the specified widget to the ones handled by the container. \
		x:        horizontal position of the widget in the container
		y:        vertical position of the widget in the container
		w:        how much of the width of the container the widget should use, in percentage
		h:        how much of the height of the container the widget should use, in percentage
		**TODO**:fit:      if True will override all other parameters and make the widget use the whole container surface
		override: whether the new widget dimensions can go over existing widgets
		hover:    if the hovered attribute of the widget should be set to True when the mouse hovers the said widget surface"""
		
		#building dimensions
		if w!=None:
			rw=int(w*self.w) #may need to change that int for blankspace may be left
		else:
			rw = widget.w

		if h!=None:
			rh=int(h*self.h)
		else:
			rh = widget.h

		assert rw<=self.w and rh<=self.h, ValueError(f"Dimensions are too big. Specified width ({w}) and height ({h}) should be inferior or equal to {self.w} and {self.h} respectively")
		rect = pg.Rect(x, y, rw, rh)

		#handling overblitting protection
		if not override:
			for widget in self.widgets.values():				
				if rect.colliderect(widget[1]):
					raise ValueError(f"Could not resolve placement of widget. Provided rect ({rect}) overlaps with other widgets. Change position/dimensions or set override.") #change with return False

		#making adapted surface
		needs_resize = False
		if rect.w==widget.w and rect.h==widget.h:
			surf = widget.surf

		else:
			needs_resize=True
			surf = pg.transform.scale(widget.surf, (rect.w, rect.h))

		#adding widget
		self.widgets[widget] = [surf, rect, needs_resize, hover]
		return rect



	def remove(self, widget):
		if self.widgets[widget][3]==True:
			self.hovered.pop(widget)
		self.widgets.pop(widget)


	def draw(self, dest, *args, **kwargs):
		"""this will draw the container and all it's widget to the dest surface in the specified location.
		Arguments can be a Rect instance or x, y, w, h integers. If no argument is provided then the container's attributes will be used."""
		if not self.visible:
			return

		self.surf=self.make_surf()
		if len(args)==0 and len(kwargs)==0:
			dest.blit(self.surf, (self.x, self.y))
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


	def update(self):
		if self.hidden:
			return
		
		#handling hovering
		mouse = pg.mouse.get_pos()
		crect = self.get_rect()
		if crect.collidepoint(mouse):
			for widget in self.hovers:
				if self.widgets[widget][1].collidepoint(mouse):
					widget.hovered=True
					break
		for widget in self.widgets:
			widget.update()

	def make_surf(self):
		"""updates the containers surface based upon the changes which happened to the widgets' surfaces"""
		for widget in self.widgets:
			if widget.changed:
				widget.changed=False
				rect = self.widgets[widget][1]
				#may be improved by checking whether the surf needs to be normalized
				surf = pg.transform.scale(widget.surf, (rect.w, rect.h))
				self.widgets[widget][0] = surf
				self.surf.blit(surf, (rect.x, rect.y))

		return self.surf

	def get_rect(self):
		return pg.Rect(self.x, self.y, self.w, self.h)

	def get_surf(self):
		"""returns a copy of the container's surface"""
		self.surf=self.make_surf()
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
	def __init__(self, w, h, alpha=False, text="", bgcolor=None, fgcolor=BLACK, font=None, font_size=20, underlined=False, bold=False, can_hover=False, max_chars=False):
		super(TextWidget, self).__init__(w, h, alpha=alpha, can_hover=can_hover)

		#text properties
		self._text = text
		self.bgcolor = bgcolor
		if bgcolor==None and alpha:
			self.bgcolor = ALPHA
		else:
			self.bgcolor = WHITE
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

	@property
	def text(self):
		return self._text

	@text.setter
	def text(self, string):
		self.changed = True
		self._text = string
		self.surf = self.render_text()

	def render_text(self):
		if self.changed:
			return self.font.render(self._text)

		return self.surf




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