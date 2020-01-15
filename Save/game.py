# A nice game

### Importations ###
import turtle
import engine
import random
import math
import time

### Global variables ###
WIDTH = 640
HEIGHT = 480
speed = 0
speedboost = 1
speeddecreasestep = 0.05
gravitystep = 0.02
gravity = 0.02
countdown = 0
angle = 90
radius = 30
skin = 'bird'   #rocket or bird
radius = 20     #20 for 'bird', 30 for 'rocket

### Classes ###
class Sun(engine.GameObject):
        def __init__(self):
                super().__init__(0, 0, 0, 0, 'sun', 'yellow')

class Ground(engine.GameObject):
        def __init__(self):
                super().__init__(0, 0, 0, 0, 'ground', 'gray')

        def heading(self):
                return 90

class Rocket(engine.GameObject):
        def __init__(self):
                super().__init__(0, 0, 0, 0, skin, 'black')

        def heading(self):
                return angle

        def move(self):

                global speed, countdown, rocket, gravity

                self.x += speed * math.cos(math.radians(180 - angle))
                self.y -= speed * math.sin(math.radians(180 - angle)) + gravity
                gravity += gravitystep

                if speed < 0:
                    speed += speeddecreasestep

                if countdown > 0 :
                        countdown -= 1
                else :
                        rocket.shape = skin

                if math.sqrt((self.y - 1170) ** 2 + self.x ** 2) < 1000 + radius:

                        banner('Game over')
                        engine.exit_engine()

                if self.y <= -220 + radius :

                        if gravity - speed > 1 or angle % 360 != 90:

                                banner('Game over')
                                engine.exit_engine()

                        else :

                                banner('You won!')
                                engine.exit_engine()

        def isoob(self):

                if super().isoob():
                        self.x = - self.x
                return False



### Functions ###
def makeshape() :

        turtle.showturtle()
        rocket = turtle.Shape("compound")
        body = ((15,0), (25.61, -10.61), (25.61, -55.61), (0, -34.5), (-25.61, -55.61), (-25.61, -10.61), (-15.5, 0))
        rocket.addcomponent(tuple((x, y + 27) for (x, y) in body), "white", "black")
        fire = ((0, -34.5), (3.35, -41.21), (0, -47.92), (-3.35, -41.21))
        rocket.addcomponent(tuple((x, y + 27) for (x, y) in fire), "orange", "orange")
        turtle.register_shape('rocket powered', rocket)


        rocket = turtle.Shape("compound")
        body = ((15,0), (25.61, -10.61), (25.61, -55.61), (0, -34.5), (-25.61, -55.61), (-25.61, -10.61), (-15.5, 0))
        rocket.addcomponent(tuple((x, y + 27) for (x, y) in body), "white", "black")
        turtle.register_shape('rocket', rocket)


        turtle.setpos(-1170, -1000)
        turtle.begin_poly()
        turtle.circle(1000)
        turtle.end_poly()
        poly = turtle.get_poly()
        turtle.register_shape('sun', poly)


        ground = turtle.Shape("compound")
        L = [(-320, -240)] + [(x, random.randrange(-220, -140)) for x in range(-320, -40,10)] + [(-40, -220), (40, -220)] + [(x, random.randrange(-220, -140)) for x in range(50, 330,10)] + [(320, -240)]
        ground.addcomponent(tuple(L), "gray", "gray")
        turtle.register_shape('ground', ground)


        body = make_circle((0, 0), 20)
        wing = make_circle((-15, 0), 20 / 3)
        eye = make_circle((12, 6), 20 / 3)
        eye2 = make_circle((15, 6), 2)
        mouth = ((6.37, -4.3), (21, -4.69), (19.5, -8.38), (4.66, -8.45), (2.95, -5.35), (2.82, -2.78), (5, 0), (18.76, -0.08), (21, -4.69), (6.37, -4.3))

        bird = turtle.Shape('compound')
        bird.addcomponent(body, 'yellow', 'black')
        bird.addcomponent(wing, 'white', 'black')
        bird.addcomponent(eye, 'white', 'black')
        bird.addcomponent(eye2, 'black', 'black')
        bird.addcomponent(mouth, 'orange', 'black')
        turtle.register_shape('bird', bird)

        bird = turtle.Shape('compound')
        bird.addcomponent(body, 'yellow', 'black')
        bird.addcomponent(wing, 'white', 'black')
        bird.addcomponent(eye, 'white', 'black')
        bird.addcomponent(eye2, 'black', 'black')
        bird.addcomponent(mouth, 'orange', 'black')
        bird.addcomponent(((-8,-22), (-8,-30)), 'black', 'black')
        bird.addcomponent(((-4,-22), (-4,-30)), 'black', 'black')
        bird.addcomponent(((0,-22), (0,-30)), 'black', 'black')
        bird.addcomponent(((8,-22), (8,-30)), 'black', 'black')
        bird.addcomponent(((4,-22), (4,-30)), 'black', 'black')
        turtle.register_shape('bird powered', bird)




def keyboard_cb(key):

        global speed, rocket, countdown, angle, gravity

        if key == 'Escape':
                engine.exit_engine()

        if key == 'Up':
                speed -= speedboost
                rocket.shape = skin + " powered"
                countdown = 20
                gravity = 0

        if key == 'Left' :
            angle += 30

        if key == 'Right' :
            angle -= 30


        if key == 'm':
                speed = 0
                rocket = Rocket()
                engine.add_obj(rocket)


def banner(msg):
    turtle.home()
    turtle.color('black')
    turtle.write(msg, True, align='center', font=('Arial', 48, 'italic'))
    time.sleep(3)
    turtle.undo()


def make_circle(point, radius):
    turtle.seth(90)
    turtle.setpos(point[0] + radius, point[1])
    turtle.begin_poly()
    turtle.circle(radius)
    turtle.end_poly()
    return turtle.get_poly()


if __name__ == '__main__':

	engine.init_screen(WIDTH, HEIGHT)
	engine.init_engine()
	makeshape()
	rocket = Rocket()
	sun = Sun()
	engine.add_obj(rocket)
	engine.add_obj(sun)
	engine.add_obj(Ground())
	engine.set_keyboard_handler(keyboard_cb)
	engine.engine()
