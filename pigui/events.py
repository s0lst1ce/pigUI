import pygame as pg

class Singleton(type):
	"""a metaclass that makes your class a a singleton"""
	_instances = {}	#dict so that different classes can inherit from the metaclass
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]


class Dispatcher(metaclass=Singleton):
	"""This object dispatches events to all widgets which need it"""
	def __init__(self):
		self.widgets = {}
		self.events = []

	def __setitem__(self, widget, events):
		self.widgets[widget] = events

	def __getitem__(self, widget):
		to_give=[]
		for event in self.events:
			if event.type in self.widgets[widget]:
				to_give.append(event)
		return to_give

	def process(self, events):
		self.events = events

SELECTED = None