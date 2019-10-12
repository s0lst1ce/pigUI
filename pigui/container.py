import pygame as pg
from pigui.colors import *
from pigui.events import *
import os

class Container(object):
	"""Container class

	x:          horizontal position used for drawing
	y:          vertical position used for drawing
	w:          width of the container
	h:          height of the container
	bgcolor:    the background color of the widet. Transparent if None. This will slow things down.
	visible:    whether the container's surface should be blitter to the screen
	background: a surface or path to image to be used as background. Path may be a string or tuple of strings"""
	def __init__(self, x, y, w, h, bgcolor=None, visible=True, background=None):
		#making sure arguments are valid
		assert not (bgcolor!=None and background!=None), ValueError("Can't set a background color & set a background surface.")
		self.x = x
		self.y = y
		self.w = w
		self.h = h

		#surface
		if background:
			if isinstance(background, pg.Surface):
				surf = background
			elif isinstance(background, tuple):
				surf = pg.image.load(os.path.join(*background)).convert()
			elif isinstance(background, str):
				surf = pg.image.load(background).convert()
			self.surf = pg.transform.scale(surf, (w, h))

		else:
			if bgcolor:
				self.bgcolor = bgcolor
			else:
				self.bgcolor = ALPHA
			self.surf = pg.Surface((w, h))
			self.surf.fill(self.bgcolor)

		self.visible = visible
		self.widgets = {}
		#an entry looks as such
		#Button: [resized_surf, area_rect, needs_resize, hover]
		#Widget: [Surface, Rect, Bool, Bool]
		self.hovered = [] #lsit of rect, widget tuples

		#misc
		self.dispatcher = Dispatcher()



	def __repr__(self):
		return f"<Container({self.x}, {self.y}, {self.w}, {self.h}) handling {len(self.widgets)} widgets ({self.widgets})>"

	@classmethod
	def from_background(cls, x, y, background, *args, **kwargs):
		if isinstance(background, pg.Surface):
			surf = background
		elif isinstance(background, tuple):
			surf = pg.image.load(os.path.join(*background)).convert()
		elif isinstance(background, str):
			surf = pg.image.load(background).convert()
		else:
			raise TypeError(f"background must be a tuple of strings representing a path to an image or a Pygame Surface not {background}")

		rect = surf.get_rect()
		return cls(x, y, rect.w, rect.h, *args, background=background, **kwargs)

	def add(self, widget, x, y, w=None, h=None, cw=None, ch=None, fit=False, override=False, events=None):
		"""adds the specified widget to the ones handled by the container. \
		x:         horizontal position of the widget in the container
		y:         vertical position of the widget in the container
		w:         resize widget width to w, in pixels
		h:         resize widget height to h, in pixels
		cw:        how much of the width of the container the widget should use, in percentage
		ch:        how much of the height of the container the widget should use, in percentage
		fit:       if True will override all other parameters and make the widget use the whole container surface **TODO**
		override:  whether the new widget dimensions can go over existing widgets"""
		#making sure arguments are valid		
		if fit:print("Ignoring 'fit' parameter")
		assert x<=100 and y<=100, ValueError("Can't place at more than 100% of the container's dimensions")
		#assert (w or h) or (cw, ch), ValueError("Can't set width and height with both ratio and pixel size")

		#building dimensions
		rw = widget.w
		rh = widget.h
		if cw or ch:
			if cw:
				rw=int((cw/100)*self.w) #may need to change that int for blankspace may be left
			if ch:
				rh=int((ch/100)*self.h)

		elif w or h:
			if w:
				rw = w
			if h:
				rh = h

		assert rw<=self.w and rh<=self.h, ValueError(f"Dimensions are too big. Specified width ({w}) and height ({h}) should be inferior or equal to {self.w} and {self.h} respectively")
		rect = pg.Rect((self.w-rw)/100*x, (self.h-rh)/100*y, rw, rh)

		#handling overblitting protection
		if not override:
			for wid in self.widgets.values():				
				if rect.colliderect(wid[1]):
					raise ValueError(f"Could not resolve placement of widget. Provided rect ({rect}) overlaps with other widgets. Change position/dimensions or set override.") #change with return False

		#making adapted surface
		needs_resize = False
		if rect.w==widget.w and rect.h==widget.h:
			surf = widget.surf

		else:
			needs_resize=True
			surf = pg.transform.scale(widget.surf, (rect.w, rect.h))

		#checking for events need
		if events:
			self.dispatcher[widget] = events
		elif hasattr(widget, "events"):
			self.dispatcher[widget] = widget.events

		#adding widget
		self.widgets[widget] = [surf, rect, needs_resize, widget.hover]
		if widget.hover:
			self.hovered.append(widget)
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
		if not self.visible:
			return
		#handling hovering
		mouse = pg.mouse.get_pos()
		crect = self.get_rect()
		for wid in self.hovered:
			wid.hovered=False

		if crect.collidepoint(mouse):
			for widget in self.hovered:
				rect = self.widgets[widget][1]
				real_rect = pg.Rect(rect.x+self.x, rect.y+self.y, rect.w, rect.h)
				if real_rect.collidepoint(mouse):
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