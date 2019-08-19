import pygame as pg
from widgets import *
from colors import *

#display
WIDTH = 800
HEIGHT = 600

pg.init()
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("A Pygame GUI library by s0lst1ce")
clock = pg.time.Clock()


#env
t = TextWidget(100, 30, text="Hello workd!", bgcolor=BLACK, fgcolor=WHITE)
c = Container(0, 0, 500, 500, bgcolor=GREEN)
c.add(t, 10, 10)
entities = [c]
running = True

#GAME LOGIC
def start():
	"""sets up the game"""
	global entities
	pass

def events():
	'''processes events'''
	global running
	pressed_keys = pg.key.get_pressed()
	for event in pg.event.get():
		if event.type == pg.QUIT or pressed_keys[pg.K_ESCAPE]:
			running=False


def update():
	'''ran each tick handles all modification based on occured events'''
	pass

def render():
	'''handles the rendering'''
	global window
	global entities
	window.fill(WHITE)
	for e in entities:
		e.draw(window)

	pg.display.flip()


def main_loop():
	'''main game logic handler'''
	global running
	global clock
	while running:
		clock.tick()
		events()
		update()
		render()

main_loop()