import pygame as pg

PYGUI_DISPATCHER = None
def get_dispatcher():
	global PYGUI_DISPATCHER
	if PYGUI_DISPATCHER==None:
		PYGUI_DISPATCHER = Dispatcher()
	return PYGUI_DISPATCHER


class Dispatcher(object):
	"""This object dispatches events to all widgets which need it
	WARNING: SHOULD ONLY BE CREATED ONCE! TRY OVERRIDING __new__ TO ASSURE THAT"""
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

PYGUI_DISPATCHER = Dispatcher()
