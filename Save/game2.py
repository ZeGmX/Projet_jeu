# A nice game

### Importations ###
import turtle
import engine
import random
import math
import time

### Global variables ###
LENGTH = 640
SPEEDBOOST = 1
SPEEDDECREASESTEP = 0.05
GRAVITYBASE = 1
GRAVITYSTEP = 0.02
GRAVITYMAX = 5
gravity = 1
COUNTDOWN = 0
LDOOR = [[[] for _ in range(5)] for _ in range(5)]
radius = 30
skin = 'bird'   #rocket or bird
radius = 20     #20 for 'bird', 30 for 'rocket
level = [[[] for _ in range(5)] for _ in range(5)]
posi = 0
posj = 4

badguys = [ [ [] for _ in range(5)] for _ in range(3)]

### Classes ###
class Rocket(engine.GameObject):

    def __init__(self):
        self.speed = 0
        self.angle = 90
        super().__init__(0, 0, 0, 0, skin, 'black')

    def heading(self):
        return self.angle

    def move(self):

        global  COUNTDOWN, rocket, gravity

        self.x += self.speed * math.cos(math.radians(180 - self.angle))
        self.y -= self.speed * math.sin(math.radians(180 - self.angle)) + gravity
        gravity = min(gravity + GRAVITYSTEP , GRAVITYMAX)

        if self.speed < 0:
            self.speed += SPEEDDECREASESTEP

        if COUNTDOWN > 0 :
            COUNTDOWN -= 1
        else :
            rocket.shape = skin


        Lplatform = self.canland()
        for landingpad in Lplatform:
            if landingpad > - LENGTH and self.y <= landingpad + radius:
                if gravity - self.speed > 1 or self.angle % 360 != 90:
                    banner('Game over')
                    engine.exit_engine()
                else:
                    self.speed = 0
                    gravity = 0


        if self.collide_gnd():
            banner('Game over')
            engine.exit_engine()


    def collide_gnd(self):
        for poly in ground.poly:
            for i in range(len(poly)):

                x1, y1 = poly[i]
                x2, y2 = poly[(i + 1) % len(poly)]
                h = 0.5   #pas de 1
                n = 0
                xi = min(x1, x2)
                yi = min(y1, y2)
                if y1 != y2:
                    if x1 == x2:
                        while  yi + n * h < max(y1, y2):
                            y = yi + n * h
                            n += 1
                            if  math.sqrt((x1 - self.x) ** 2 + (y - self.y) ** 2) < radius:
                                return True

                    else:
                        m = (y1 - y2) / (x1 - x2)
                        p = y2 - m * x2

                        while xi + n * h < max(x1, x2):
                            x = xi + n * h
                            y = m * x + p
                            n += 1

                            if math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2) < radius:
                                return True

        return False


    def canland(self):
        Lplatform = []
        for poly in ground.poly:
            tempres = False
            for i in range(len(poly)):
                x1, y1 = poly[i]
                x2, y2 = poly[(i + 1) % len(poly)]
                if y1 == y2 and abs(x2 - x1) == 80 and self.x - radius > min(x1, x2) and self.x + radius < max(x1, x2) and self.y > y1:
                    tempres = True
                    Lplatform.append(y1)
            if not tempres:
                Lplatform.append(- LENGTH)
        return Lplatform



    def isoob(self):
        global ground, posi, posj
        if super().isoob():
            for door in LDOOR[posi][posj]:
                engine.del_obj(door)
            if self.y < -300:
                posi += 1
                self.y = 280
            elif self.y > 300:
                posi -= 1
                self.y = -280
            elif self.x < -300:
                posj -= 1
                self.x = 280
            elif self.x > 300:
                posj += 1
                self.x = -280
        engine.del_obj(ground)
        ground = Ground(level[posi][posj])
        for door in LDOOR[posi][posj]:
            engine.add_obj(door)

        return False


class Ground(engine.GameObject):

    def __init__(self, compounds=[]):
        self.poly = compounds
        ground = turtle.Shape('compound')
        for poly in compounds:
            poly = tuple((-y, x) for (x, y) in poly)
            ground.addcomponent(poly, 'black')
        turtle.register_shape('ground', ground)
        super().__init__(0, 0, 0, 0, 'ground', 'black')


class Door(engine.GameObject):
    def __init__(self, x, y, color):
        super().__init__(x, y, 0, 0, 'door', color)


class BadGuy(engine.GameObject) :

    def __init__(self,x ,y) :
        self.countdown = 0
        self.seuil = 100
        super().__init__(x, y, 0, 0, 'badguy', 'black')

    def move(self) :
        
        self.countdown += 1
        if self.countdown > self.seuil :
            self.seuil = 100
            self.countdown = 0
            enplus = 0
            if self.x < rocket.x :
                enplus = 180
            if self.x == rocket.x :
                angle = 0
            else :
                angle = enplus +  math.degrees(math.atan((self.y - rocket.y) / (self.x - rocket.x)))
            engine.add_obj(Bullet(self.x, self.y, angle))

class NiceBullet(engine.GameObject) :

    def __init__(self, x, y, angle) :
        self.angle = angle
        self.speed = 3
        self.radius = 5
        super().__init__(x, y, 0, 0, 'graybullet', 'black')

    def move(self) :

        self.x += self.speed * math.cos(math.radians(180 - self.angle))
        self.y -= self.speed * math.sin(math.radians(180 - self.angle))

        for badguy in badguys :
            if self.collide(badguy) :
                engine.del_obj(badguy)
                self.shape = 'whitebullet'
                engine.del_obj(self)

        if self.collide_gnd() :
            self.shape = 'whitebullet'
            engine.del_obj(self)
            
    def collide(self, badguy) :
        if math.sqrt( (self.x - badguy.x)**2 + (self.y - badguy.y)**2) < radius + self.radius :
            return True

    def collide_gnd(self):
        for poly in ground.poly:
            for i in range(len(poly)):

                x1, y1 = poly[i]
                x2, y2 = poly[(i + 1) % len(poly)]
                h = 0.5   #pas de 1
                n = 0
                xi = min(x1, x2)
                yi = min(y1, y2)
                if y1 != y2:
                    if x1 == x2:
                        while  yi + n * h < max(y1, y2):
                            y = yi + n * h
                            n += 1
                            if  math.sqrt((x1 - self.x) ** 2 + (y - self.y) ** 2) < self.radius :
                                return True

                    else:
                        m = (y1 - y2) / (x1 - x2)
                        p = y2 - m * x2

                        while xi + n * h < max(x1, x2):
                            x = xi + n * h
                            y = m * x + p
                            n += 1

                            if math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2) < self.radius:
                                return True

        return False
    
        
class Bullet(engine.GameObject) :

    def __init__(self, x, y, angle) :
        self.angle = angle
        self.speed = 3
        self.radius = 5
        super().__init__(x, y, 0, 0, 'graybullet', 'black')

    def move(self) :

        self.x += self.speed * math.cos(math.radians(180 - self.angle))
        self.y -= self.speed * math.sin(math.radians(180 - self.angle))
        
        if self.collide() :
            banner('Game over')
            engine.exit_engine()

        if self.collide_gnd() :
            self.shape = 'whitebullet'
            engine.del_obj(self)
    
            
    def collide(self) :
        if math.sqrt( (self.x - rocket.x)**2 + (self.y - rocket.y)**2) < radius + self.radius :
            return True

    def collide_gnd(self):
        for poly in ground.poly:
            for i in range(len(poly)):

                x1, y1 = poly[i]
                x2, y2 = poly[(i + 1) % len(poly)]
                h = 0.5   #pas de 1
                n = 0
                xi = min(x1, x2)
                yi = min(y1, y2)
                if y1 != y2:
                    if x1 == x2:
                        while  yi + n * h < max(y1, y2):
                            y = yi + n * h
                            n += 1
                            if  math.sqrt((x1 - self.x) ** 2 + (y - self.y) ** 2) < self.radius :
                                return True

                    else:
                        m = (y1 - y2) / (x1 - x2)
                        p = y2 - m * x2

                        while xi + n * h < max(x1, x2):
                            x = xi + n * h
                            y = m * x + p
                            n += 1

                            if math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2) < self.radius:
                                return True

        return False

badguys[0][3] = [BadGuy(-100,225)]


        
        
        


    
### Functions ###
def make_circle(point, radius):
    turtle.seth(90)
    turtle.setpos(point[0] + radius, point[1])
    turtle.begin_poly()
    turtle.circle(radius)
    turtle.end_poly()
    return turtle.get_poly()

def banner(msg):
    turtle.home()
    turtle.color('darkblue')
    turtle.write(msg, True, align='center', font=('Arial', 48, 'italic'))
    time.sleep(3)
    turtle.undo()


def makeshape():

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

    bullet = turtle.Shape('compound')
    bullet.addcomponent(make_circle((0, 0), 5), 'darkgray', 'darkgray')
    bullet.addcomponent(make_circle((-1,1), 3.59), 'lightgray', 'lightgray')
    turtle.register_shape('graybullet', bullet)

    bullet = turtle.Shape('compound')
    bullet.addcomponent(make_circle((0, 0), 5), 'white', 'white')
    turtle.register_shape('whitebullet', bullet)

    badguy = turtle.Shape('compound')
    badguy.addcomponent(make_circle((-2, 2), 20), 'red', 'red')
    badguy.addcomponent(make_circle((-5, 5), 10), 'pink', 'pink')
    turtle.register_shape('badguy', badguy)

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


    door = ((-25, 100), (25,100), (42, 58), (46, 13), (26, 13), (26, -13), (42, -58), (25, -100), (-25, -100), (-42, -58), (-46, -13), (-46, 13), (-42, 58))
    door = tuple((-y, x) for (x, y) in door)
    turtle.register_shape('door', door)

    poly = ((-250,-100), (-214,-194), (-137, -263), (-66, -210), (-26, -255), (39, -213), (72, -152), (152, -152), (236, -115), (261, -21), (228, 19), (272, 102), (263, 197), (200, 262), (113, 241), (79, 262), (30, 259), (-44, 223), (-137, 232), (-202, 261), (-232, 152), (-250, 100),  (-400, 100), (-400, 400), (400, 400), (400, -400), (-400, -400), (-400, -100))
    level[0][4].append(poly)

    poly = ((250, 100), (100, 243), (0, 200), (-21, 148), (-69, 228), (-183, 257), (-310, 185), (-400, 190), (-400, 400), (400, 400), (400, 100))
    level[0][3].append(poly)
    poly = ((250,-100), (200, -200), (179, -291), (200, -400), (400, -400), (400, -100))
    level[0][3].append(poly)
    poly = ((-48, -345), (-92, -263), (-181, -219), (-247, -116), (-382, -96), (-400, -400))
    level[0][3].append(poly)

    poly = ((350, 190), (280, 227), (184, 266), (118, 251), (-16, 227), (-69, 227), (-153, 248), (-200, 200), (-257, 116), (-307, 89), (-296, 26), (-233,-45), (-267, -114), (-200, -200), (-220, -400), (-400, -400), (-400, 400), (400, 400))
    level[0][2].append(poly)
    poly = ((87, -336), (131, -209), (224, -106), (354, -66), (400, -400))
    level[0][2].append(poly)

    poly = ((-350, 178), (-235, 240), (-119, 273), (-84, 145), (-19, 278), (99, 235), (186, 262), (280, 186), (302, 91), (222, 91), (178, 29), (272, -24), (283, -162), (202, -246), (29, -227), (-54, -270), (-320, -224), (-400, -400), (400, -400), (400, 400), (-400, 400))
    level[1][4].append(poly)

    poly = ((-320, 320), (-100, 320), (-100, 250), (-178, 277), (-215, 138), (-280, 200), (-297, 178), (-320, 97))
    level[1][1] .append(poly)
    poly = ((100, 320), (100, 250), (177, 256), (203, 175), (239, 196), (250, 100), (320, 100), (320, 320))
    level[1][1].append(poly)
    poly = ((320, -100), (320, -320), (-57, -320), (20, -223), (83, -241), (139, -164), (201, -179), (250, -100))
    level[1][1].append(poly)
    poly = ((-320, -130), (-278, -179), (-237, -261), (-320, -320))
    level[1][1].append(poly)

    poly = (-180,150), (-100, 150), (-59, 179), (21, 138), (0, 57), (-101, 41), (-119, -21), (-141, 0), (-200, 37), (-220, 117)
    level[0][1].append(poly)
    poly = (-100, -320), (-100, -250), (-199, -220), (-222, -162), (-279, -141), (-299, 15), (-278, 260), (-37, 317), (218, 278), (259, 158), (221, 20), (259, -41), (237, -119), (180, -183), (100, -250), (100, -320), (320, -320), (320, 320), (-320, 320), (-320, -320)
    level[0][1].append(poly)

    poly = ((320, -320), (-10, -320), (-81, -101), (-59, 96), (41, 120), (61, 178), (100, 100), (120, -63), (200, -63), (220, 57), (157, 258), (-81, 304), (-200, 200), (-241, -44), (-264, -320), (-320, -320), (-320, 320), (320, 320))
    level[0][0].append(poly)

    poly = ((-10, 320), (56, 196), (238, 180), (320, 97), (320, 320))
    level[1][0].append(poly)
    poly = ((320, -130), (302, -158), (223, -184), (162, -280), (140, -320), (320, -320))
    level[1][0].append(poly)
    poly = ((-100, -320), (-143, -203), (-219, -180), (-279, -43), (-280, 198), (-264, 320), (-320, 320), (-320, -320))
    level[1][0].append(poly)
    poly = ((-150, 100), (-70, 100), (62, 79), (45, 0), (-60, -43), (-78, -103), (-119, 0), (-201, 60))
    level[1][0].append(poly)

    poly = ((200, 350), (210, 300), (225, 236), (255, 190), (381, 200), (395, 352))
    level[1][3].append(poly)
    poly = ((-70, 300), (-76, 169), (-181, 174), (-290, 59), (-272, -202), (-162, -282), (47, -151), (162, -106), (285, -127), (400, -127), (400, -400), (-400, -400), (-400, 400), (-70, 400))
    level[1][3].append(poly)
    poly = ((39, 94), (-23, 59), (-41, -41), (51, -86), (147, -16), (109, 64))
    level[1][3].append(poly)

    poly = ((-184, 285), (-224, 230), (-250, 100), (-400, 100), (-400, 400), (-200, 400))
    level[1][2].append(poly)
    poly = ((-250, -100), (-200, -200), (-63, -247), (102, -287), (142,-146), (242, -101), (263, 23), (242, 174), (152, 199), (107, 282), (110, 400), (400, 400), (400, -400), (-400, -400), (-400, -100))
    level[1][2].append(poly)






def keyboard_cb(key):

    global rocket, COUNTDOWN, gravity

    if key == 'Escape':
        engine.exit_engine()

    if key == 'Up':
        rocket.speed -= SPEEDBOOST
        rocket.shape = skin + " powered"
        COUNTDOWN = 20
        gravity = max(0, gravity - 1)

    if key == 'Left' :
        rocket.angle += 30

    if key == 'Right' :
        rocket.angle -= 30

    if key == 'space' :
        engine.add_obj(NiceBullet(rocket.x, rocket.y, 90 + rocket.angle))
        

if __name__ == '__main__':

    engine.init_screen(LENGTH, LENGTH)
    engine.init_engine()
    makeshape()
    rocket = Rocket()
    ground = Ground(level[posi][posj])
    engine.add_obj(ground)
    engine.add_obj(rocket)
    badguys = [BadGuy(-100,225)]
    for badguy in badguys :
        engine.add_obj(badguy)
    engine.set_keyboard_handler(keyboard_cb)
    engine.engine()





