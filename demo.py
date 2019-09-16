import pygame as pg
from pigui import *
from pigui.colors import *
import inspect
import time

#display
WIDTH = 800
HEIGHT = 600

pg.init()
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("A Pygame GUI library by s0lst1ce")
clock = pg.time.Clock()
base_path = os.path.join("demo", "png")

t1 = time.time()
#env
dispatcher = Dispatcher.get()
t = Label.from_background(os.path.join(base_path, "button", "blank", "textbg2.png"), text="Hello World!", offset=(25, 0))
b = TextButton(100,50, action=lambda:print("Hello"), text="World", fgcolor=ORANGE_RED, alpha=True)
b2 = ImageButton.from_image(os.path.join(base_path, "button", "like1.png"), action=lambda:print("Like"), high_image=os.path.join(base_path, "button", "like2.png"))
c = Container(50, 0, 500, 400, background=(base_path, "windows", "Window", "win6.png"))
c.add(t, 50, 16)#, w=150, h=50)
c.add(b, 80, 80)
c.add(b2, 0, 100)
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