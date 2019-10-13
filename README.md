<p align="center">
  <img width="256" height="256" src="https://github.com/s0lst1ce/assets/blob/master/pig.png">
</p>

# pigUI

pigUI is a GUI toolkit for [Pygame](https://www.pygame.org/news). It provides objects that enables anyone to easily implement a GUI into their game without having to modify their game logic in any major way.

​	To do this pigUI provides a set of widgets such as Labels and Buttons which are organized into Containers. Containers are like "boxes" into which you can put your widgets. All widgets must be contained in order to be displayed.



## Quickstart

To demonstrate how the library works, a `demo.py` example program has been made. In this quick preview we'll explain the principles used in the demo.

### Setting up environment

Although this won't be the case in bigger games the demo defines all widgets at the beginning of the program.

```python
import pygame as pg
from pigui import *

#display
WIDTH = 800
HEIGHT = 600
pg.init()
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("A Pygame GUI library by s0lst1ce")
clock = pg.time.Clock()
running = True

#env
dispatcher = Dispatcher.get()
c = Container.from_background(50, 10, os.path.join("..", "png", "windows", "Window", "win6.png"))
t = Label.from_background(os.path.join("..", "png", "button", "blank", "textbg1.png"), text="Hello World!", offset=(25, 0))
c.add(t, 50, 16)
entities = [c]
```

The 11 first lines are just Pygame display setup, the interesting part comes after that. There are two objects that will be created with pigUI which aren't widgets. The first one is Dispatcher. This object will process all events for the library and will need to be integrated to the event loop. But more on that in the next section. Just remember that you need to call the `get()` classmethod on it.

Next comes the Container. As explained earlier this is like a box into which the widgets will be put. Here we create it from a background image. The first two parameters represents the coordinates at which the container should be placed. This can be changed later on. Next comes the path to the background image to load. This can also be a Pygame Surface.

Finally we create our widgets and add them the container. 



### The event loop

To function properly pigUI requires an event loop. Since almost every game has one anyways this shouldn't be a problem in most cases. If you already have one: don't worry. You'll only need to add one line. The event loop loop of the demo is the following:

```python
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
```



As you can see the only place where pigUI is involved is at the last lines. And that's really all that needs to be done event-wise. Supply all events which occurred this tick to the dispatcher's `process` method and you're done with it. This allows you to keep your logic readable and concise at the same time.



### The main loop

Now comes the core of every game: the main loop. Also called the game loop, this is where the game's logic happens. In the major part it exists to update the different objects your game is made of. pigUI uses it to update it's widgets. However to keep it simple and concise it was built in such way that you only need to call the `update` method of all your containers. They will themselves determine if their widgets need to be updated, how and when.

```python
def update():
	'''ran each tick handles all modification based on occured events'''
	global entities
	for entity in entities:
		entity.update()
```



### Rendering

Finally the widgets and containers need to be rendered or you'll have done all this work for nothing. Once again this has been kept as simple as possible since you only need to call your containers' `draw` method. It takes a single parameter: the surface to draw the container to. This can be the display.

```python
def render():
	'''handles the rendering'''
	global window
	global entities
	window.fill(BLUE)
	for e in entities:
		e.draw(window)

	pg.display.flip()
```
