import pygame as pg
from pygui import *
from colors import *
import inspect
import time

#display
WIDTH = 800
HEIGHT = 600

pg.init()
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("A Pygame GUI library by s0lst1ce")
clock = pg.time.Clock()

t1 = time.time()
#env
dispatcher = Dispatcher.get()
#t = Label(150, 30, text="PyGUI!", bold=True, alpha=True)
t = Label.from_background(os.path.join("..", "png", "button", "blank", "textbg1.png"), text="Hello World!", offset=(25, 0))
b = TextButton(100,50, action=lambda:print("Hello"), text="World", fgcolor=BLACK, alpha=True)
h = HighlightedLabel.from_background(os.path.join("..", "png", "button", "blank", "textbg2.png"), text="BOOM!", offset=(25, 0))
#c = Container.from_background(50, 10, os.path.join("..", "png", "windows", "Window", "win6.png"))
c = Container(50, 0, 500, 400, background=("..", "png", "windows", "Window", "win6.png"))
c.add(t, 50, 16)#, w=150, h=50)
c.add(b, 80, 80)
c.add(h, 0, 80)
entities = [c]
running = True
#print(c, t, b)


#GAME LOGIC
def start():
	"""sets up the game"""
	global entities
	pass

def events():
	'''processes events'''
	global running
	global dispatcher

	pressed_keys = pg.key.get_pressed()
	events = pg.event.get()
	for event in events:
		if event.type == pg.QUIT or pressed_keys[pg.K_ESCAPE]:
			running=False

	dispatcher.process(events)


def update():
	'''ran each tick handles all modification based on occured events'''
	global entities
	global t1
	global t
	if time.time()-t1>1:
		t.text= "Bonjour"
	for entity in entities:
		entity.update()

def render():
	'''handles the rendering'''
	global window
	global entities
	window.fill(BLUE)
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