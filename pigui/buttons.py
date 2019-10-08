import pygame as pg
from pigui.widgets import *
from pigui.colors import *
from pigui.labels import Label

class AbstractButton(Widget):
	"""docstring for Button"""
	def __init__(self, w, h, *args, alpha=False, action=None, locked=False, **kwargs):
		super().__init__(w, h, *args, alpha=alpha, **kwargs)
		self.w = w
		self.h = h
		assert action!=None, TypeError(f"Action must be a function (lambda or else), not {action}")
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
			events = Dispatcher()[self]
			if events:
				self.action()


class TextButton(AbstractButton, Label):
	"""a button with text"""
	def __init__(self, w, h, *args, alpha=False, action=None, text="", bgcolor=None, fgcolor=BLACK, font=None, font_size=20, underlined=False, bold=False, highlight_color=None, lock_color=LIGHT_GREY, **kwargs):
		super().__init__(w, h, *args, alpha=alpha, action=action, text=text, bgcolor=bgcolor, fgcolor=fgcolor, font=font, font_size=font_size, underlined=underlined, bold=bold, **kwargs)
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

	@classmethod
	def from_background(cls, background, *args, **kwargs):
		surf = load_surf(background)
		rect = surf.get_rect()
		return cls(rect.w, rect.h, *args, background=background, **kwargs)


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

class ImageButton(AbstractButton):
	"""docstring for ImageButton"""
	def __init__(self, w, h, alpha=False, action=None, locked=False, image=None, high_image=None):
		super().__init__(w, h, alpha=alpha, action=action, locked=locked, image=image, high_image=high_image)
		if not image:
			raise TypeError("Image must be a Pygame Surface or a path to an image")
		self.image = load_surf(image)
		if not high_image:
			self.high_image = self.image.copy()
		else:
			self.high_image = load_surf(high_image)

		#surface
		self.surf = self.image.copy()
		self.was_hovered = False

	@classmethod
	def from_image(cls, image, *args, **kwargs):
		"""find a way to re-use the code in the Label class"""
		surf = load_surf(image)
		rect = surf.get_rect()
		return cls(rect.w, rect.h, *args, image=surf, **kwargs)

	@property
	def locked(self):
		return self.AbstractButton.locked()

	def update(self):
		super().update()
		if not self._locked and self.hovered:
			self.surf = self.high_image
			self.changed = True
			self.was_hovered=True
		
		elif self.was_hovered:
			self.surf = self.image
			self.changed = True
			self.was_hovered=False