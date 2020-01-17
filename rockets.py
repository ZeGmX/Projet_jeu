import engine
import game
import math
import shapes


class Rocket(engine.GameObject):
    SPEEDBOOST = 1
    SPEEDDECREASESTEP = 0.05
    GRAVITYBASE = 1
    GRAVITYSTEP = 0.02
    GRAVITYMAX = 5
    NBLIVES = 3
    gravity = 1
    countdown = 0
    skin = 'bird'   #rocket or bird
    radius = 20     #20 for 'bird', 30 for 'rocket
    debuginit = 0

    def __init__(self):
        self.speed = 0  #Turn this into a vector ?
        self.angle = 90
        self.lives = Rocket.NBLIVES
        self.radius = Rocket.radius
        super().__init__(0, 0, 0, 0, Rocket.skin, 'black')

    def heading(self):
        return self.angle

    def rocket_up(self):
        "when the up arrow is pressed"
        self.speed -= Rocket.SPEEDBOOST
        self.shape = Rocket.skin + " powered"
        Rocket.countdown = 20
        Rocket.gravity = max(0, Rocket.gravity - 1)

    def rocket_left(self):
        self.angle += 30

    def rocket_right(self):
        self.angle -= 30

    def move(self):
        #global  countdown, gravity
        game.gameplay(self)

        self.x += self.speed * math.cos(math.radians(180 - self.angle))
        self.y -= self.speed * math.sin(math.radians(180 - self.angle)) + Rocket.gravity
        Rocket.gravity = min(Rocket.gravity + Rocket.GRAVITYSTEP , Rocket.GRAVITYMAX)

        if self.speed < 0:  #Natural slowing down
            self.speed += Rocket.SPEEDDECREASESTEP

        if Rocket.countdown > 0:
            Rocket.countdown -= 1
        else:
            self.shape = Rocket.skin


        Lplatform = self.canland()
        for landingpad in Lplatform:
            if landingpad > - game.LENGTH and self.y <= landingpad + Rocket.radius:
                if Rocket.gravity - self.speed > 1 or self.angle % 360 != 90:
                    self.losealife()
                else:
                    Rocket.gravity = 0
                    self.speed = 0


        if shapes.collide_gnd(self) or shapes.collide_door(self):
            self.losealife()


    def losealife(self):
        #global gravity, posi, posj, ground
        if self.lives == 0:
            game.banner('Game over')
            engine.exit_engine()
        else:
            self.lives -= 1
            self.speed = 0
            self.angle = 90
            self.x = 0
            self.y = 0
            self.skin = Rocket.skin
            Rocket.gravity = Rocket.GRAVITYBASE
            game.banner("Life lost, {} remaining".format(self.lives))
            game.posi = 0
            game.posj = 4
            game.load()

    def canland(self):
        Lplatform = []
        for poly in game.ground.poly:
            tempres = False
            for i in range(len(poly)):
                x1, y1 = poly[i]
                x2, y2 = poly[(i + 1) % len(poly)]
                if y1 == y2 and abs(x2 - x1) == 80 and self.x - Rocket.radius > min(x1, x2) and self.x + Rocket.radius < max(x1, x2) and self.y > y1:
                    tempres = True
                    Lplatform.append(y1)
            if not tempres:
                Lplatform.append(- game.LENGTH)
        return Lplatform


    def isoob(self):
        #global ground, posi, posj, debuginit, bosshere
        if super().isoob():
            if self.y < -300:
                game.posi += 1
                self.y = 280
            elif self.y > 300:
                game.posi -= 1
                self.y = -280
            elif self.x < -300:
                game.posj -= 1
                self.x = 280
            elif self.x > 300:
                game.posj += 1
                self.x = -280
            game.load()

        #elif Rocket.debuginit < 2:         #Weird problems when first loading
        for (door , _, _) in shapes.Door.ldoor[game.posi][game.posj]:
            engine.add_obj(door)
        for key in shapes.Key.lkey[game.posi][game.posj]:
            engine.add_obj(key)
            #Rocket.debuginit += 1

        return False
