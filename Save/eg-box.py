# basic moving box


import turtle
import engine
import random
from math import sqrt

WIDTH = 640
HEIGHT = 480
speed = 0
class Sun(engine.GameObject):
        def __init__(self):
                super().__init__(-26, (HEIGHT/2) -50, 0, 0, 'sun', 'yellow')

class Box(engine.GameObject):
        def __init__(self):
                super().__init__(0, 0, 0, 0, 'rocket', 'red')

        def heading(self):
                return 90

        def move(self):
                global speed
                self.y -= speed
                speed += 0.05

def makeshape() :
        B = 15
        turtle.begin_poly()
        turtle.fd(B)
        turtle.rt(45)
        turtle.fd(sqrt(2)*B)
        turtle.rt(45)
        turtle.fd(4 * B)
        turtle.rt(135)
        turtle.fd(sqrt(8)*B)
        turtle.rt(45)
        turtle.fd(3*B)
        turtle.lt(90)
        turtle.fd(B)
        turtle.lt(45)
        turtle.fd(sqrt(2)*B)
        turtle.lt(45)
        turtle.fd(4 * B)
        turtle.lt(135)
        turtle.fd(sqrt(8)*B)

        turtle.end_poly()
        poly = turtle.get_poly()
        turtle.register_shape('rocket', poly)

        turtle.begin_poly()
        turtle.circle(100, 360)
        turtle.end_poly()
        poly = turtle.get_poly()
        turtle.register_shape('sun', poly)



def keyboard_cb(key):
        global speed
        if key == 'Escape':
                engine.exit_engine()
        if key == 'space':
                speed -= 5
        if key == 'm' :
                speed = 0
                box = Box()
                engine.add_obj(box)


if __name__ == '__main__':
	engine.init_screen(WIDTH, HEIGHT)
	engine.init_engine()
	makeshape()
	car = Box()
	engine.add_obj(car)
	engine.add_obj(Sun())
	engine.set_keyboard_handler(keyboard_cb)
	engine.engine()
