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
countdown = 0
NBLIVES = 3
gravity = 1


level = [[[] for _ in range(5)] for _ in range(3)]


radius = 30
skin = 'bird'   #rocket or bird
radius = 20     #20 for 'bird', 30 for 'rocket
posi = 0
posj = 4


debuginit = 0




### Classes ###
class Rocket(engine.GameObject):

    def __init__(self):
        self.speed = 0
        self.angle = 90
        self.lives = NBLIVES
        self.radius = radius
        super().__init__(0, 0, 0, 0, skin, 'black')

    def heading(self):
        return self.angle

    def move(self):

        global  countdown, gravity


        gameplay(self)

        self.x += self.speed * math.cos(math.radians(180 - self.angle))
        self.y -= self.speed * math.sin(math.radians(180 - self.angle)) + gravity
        gravity = min(gravity + GRAVITYSTEP , GRAVITYMAX)

        if self.speed < 0:
            self.speed += SPEEDDECREASESTEP

        if countdown > 0 :
            countdown -= 1
        else :
            rocket.shape = skin


        Lplatform = self.canland()
        for landingpad in Lplatform:
            if landingpad > - LENGTH and self.y <= landingpad + radius:
                if gravity - self.speed > 1 or self.angle % 360 != 90:
                    self.losealife()
                else:
                    gravity = 0
                    self.speed = 0


        if collide_gnd(self) or collide_door(self):
            self.losealife()


    def losealife(self):
        global gravity, posi, posj, ground
        if self.lives == 0:
            banner('Game over')
            engine.exit_engine()
        else:
            self.lives -= 1
            self.speed = 0
            self.angle = 90
            self.x = 0
            self.y = 0
            gravity = GRAVITYBASE
            banner("Life lost, {} remaining".format(self.lives))
            posi = 0
            posj = 4
            load()

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
        global ground, posi, posj, debuginit, bosshere
        if super().isoob():

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

            load()

        elif debuginit < 2:         #Weird problems when first loading
            for (door , _, _) in ldoor[posi][posj]:
                engine.add_obj(door)
            for key in lkey[posi][posj]:
                engine.add_obj(key)
            debuginit += 1

        return False






### Functions ###

def banner(msg):
    turtle.home()
    turtle.color('darkblue')
    turtle.write(msg, True, align='center', font=('Arial', 48, 'italic'))
    time.sleep(1)
    turtle.undo()

def keyboard_cb(key):

    global rocket, countdown, gravity

    if key == 'Escape':
        engine.exit_engine()

    if key == 'Up':
        rocket.speed -= SPEEDBOOST
        rocket.shape = skin + " powered"
        countdown = 20
        gravity = max(0, gravity - 1)

    if key == 'Left' :
        rocket.angle += 30

    if key == 'Right' :
        rocket.angle -= 30


    if key == 'm':
        rocket.speed = 0
        rocket = Rocket()
        engine.add_obj(rocket)

    if key == 'space' :
        engine.add_obj(NiceBullet(rocket.x, rocket.y, 90 + rocket.angle))



def load():
    global ground, bosshere, bullets
    engine.del_obj(ground)
    ground = Ground(level[posi][posj])
    for i in range(3):
        for j in range(5):
            if i != posi or j != posj:
                for (door, _, _) in ldoor[i][j]:
                    engine.del_obj(door)
                for key in lkey[i][j]:
                    engine.del_obj(key)
                for badguy in badguys[i][j]:
                    engine.del_obj(badguy)
    for bullet in bullets:
        engine.del_obj(bullet)
    bullets = []

    for _ in range(3):
        for badguy in badguys[posi][posj]:
            engine.add_obj(badguy)
        for (door , _, _) in ldoor[posi][posj]:
            engine.add_obj(door)
        for key in lkey[posi][posj]:
            engine.add_obj(key)



    if posi == 2 and posj == 3 and bossbeaten == 0 and boss.life > 0 and bosshere < 2:
        engine.add_obj(boss)
        bosshere += 1
    if (posi != 2 or posj != 3)  and bossbeaten == 0:
        bosshere = 0




def gameplay(self):
        global pickedupkeys, doorsopened, lkey

        pickupkey(0, 4, 0, 0, 4, -268, 0)
        dooropening(0, 4, 1, 0, -300, 0, 0, 10)
        pickupkey(1, 4, 1, 1, 2, -268, 0)
        dooropening(1, 2, 2, 1, -300, 0, 0, 10)
        pickupkey(0, 0, 2, 1, 1, 0, 268)
        dooropening(1, 1, 3, 2, 0, 300, 10, 0)
        pickupkey(0, 1, 3, 2, 2, 268, 0)
        dooropening(2, 2, 4, 3, 300, 0, 0, 10)

        if bossbeaten == 1:
            if ldoor[2][3] != []:
                (door, x, y) = ldoor[2][3][0]
                key = lkey[2][3][0]
                if door.y < 400:
                    door.y += 10
                    key.y += 10
                else:
                    engine.del_obj(door)
                    engine.del_obj(key)
                    ldoor[2][3].remove((door, x, y))
                    lkey[2][3].remove(key)

        if posi == 2 and posj == 4:
            banner('You won!')
            engine.exit_engine()


if __name__ == '__main__':

    engine.init_screen(LENGTH, LENGTH)
    engine.init_engine()
    makeshape()
    create_doors_keys()
    create_badguys()
    rocket = Rocket()
    boss = Boss(30, 0)
    engine.del_obj(boss)
    ground = Ground(level[posi][posj])
    engine.add_obj(ground)
    engine.add_obj(rocket)
    #badguys = [BadGuy(-100, 225)]
    #badguys = []
    engine.set_keyboard_handler(keyboard_cb)
    load()
    engine.engine()
