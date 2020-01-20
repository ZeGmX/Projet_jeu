import game, math
import engine, shapes, bad_guys


class Rocket(engine.GameObject):
    SPEEDBOOST = 0.6
    SPEEDDECREASESTEP = 0.02
    GRAVITYSTEP = 0.02
    NBLIVES = 3
    skin = 'bird'   #rocket or bird
    radius = 20     #20 for 'bird', 30 for 'rocket
    debuginit = 0

    def __init__(self):

        self.speed = [0, 0] #v_x, v_y
        self.angle = 90
        self.lives = Rocket.NBLIVES
        self.radius = Rocket.radius
        self.landed = False
        self.countdown = 0
        super().__init__(0, 0, 0, 0, Rocket.skin, 'black')

    def init_rockets():
        assert game.Game.rocket == "", "rocket already initialized"
        print("Initializing the rocket...")
        game.Game.rocket = Rocket()

    def heading(self):
        return self.angle

    def rocket_up(self):
        "when the up arrow is pressed"
        self.speed[0] -= Rocket.SPEEDBOOST * math.cos(math.radians(180 - self.angle))
        self.speed[1] -= Rocket.SPEEDBOOST * math.sin(math.radians(180 - self.angle))
        self.shape = Rocket.skin + " powered"
        self.countdown = 20
        self.landed = False

    def rocket_left(self):
        self.angle += 30
        self.landed = False

    def rocket_right(self):
        self.angle -= 30
        self.landed = False

    def move(self):

        if not (game.Game.pause or game.Game.freeze_spawn):

            game.gameplay(self)

            self.x += self.speed[0]
            self.y -= self.speed[1]
            self.speed[1] += Rocket.GRAVITYSTEP

            if self.speed[1] < 0:  #Natural slowing down - friction
                self.speed[1] += Rocket.SPEEDDECREASESTEP / 2
            if self.speed[0] < 0:
                self.speed[0] += Rocket.SPEEDDECREASESTEP  #less friction horizontally
            elif self.speed[0] > 0:
                self.speed[0] -= Rocket.SPEEDDECREASESTEP

            if self.countdown > 0: #display bac the unpowered skin
                self.countdown -= 1
            else:
                self.shape = Rocket.skin

            if not self.landed:
                if shapes.collide_gnd(self) or shapes.collide_door(self):
                    self.losealife()
                Lplatform = self.canland()
                for landingpad in Lplatform:
                    if landingpad > - game.Game.LENGTH and self.y <= landingpad + Rocket.radius:
                        if abs(self.speed[1]) > 0.8 or self.angle % 360 != 90:
                            self.losealife()
                        else:
                            self.land()

            else:
                self.land()

    def land(self):
        self.speed[1] = self.speed[0] = 0
        self.landed = True

    def losealife(self):
        if self.lives == 0:
            game.banner('Game over')
            engine.exit_engine()
            game.Stats.display_stats()
        else:
            self.lives -= 1
            self.speed[0] = self.speed[1] = 0
            self.angle = 90
            self.x = 0
            self.y = 0
            self.skin = Rocket.skin
            game.Game.freeze_spawn = True
            game.banner("Life lost, {} remaining".format(self.lives))
            if game.Game.posi == 2 and game.Game.posj == 3 and not bad_guys.Boss.bossbeaten:
                engine.del_obj(game.Game.boss)
            game.Game.posi = 0
            game.Game.posj = 4
            game.load()

    def canland(self):
        Lplatform = []
        for poly in game.Game.ground.poly:
            tempres = False
            for i in range(len(poly)):
                x1, y1 = poly[i]
                x2, y2 = poly[(i + 1) % len(poly)]
                if y1 == y2 and abs(x2 - x1) == 80 and self.x - Rocket.radius > min(x1, x2) and self.x + Rocket.radius < max(x1, x2) and self.y > y1:
                    tempres = True
                    Lplatform.append(y1)
            if not tempres:
                Lplatform.append(- game.Game.LENGTH)
        return Lplatform


    def isoob(self):
        "out of bond management"
        if super().isoob():
            if self.y < -300:
                game.Game.posi += 1
                self.y = 280
            elif self.y > 300:
                game.Game.posi -= 1
                self.y = -280
            elif self.x < -300:
                game.Game.posj -= 1
                self.x = 280
            elif self.x > 300:
                game.Game.posj += 1
                self.x = -280
            game.load()

        elif Rocket.debuginit < 2:         #Weird problems when first loading
            for door in shapes.Door.ldoor[game.Game.posi][game.Game.posj]:
                engine.add_obj(door)
            for key in shapes.Key.lkey[game.Game.posi][game.Game.posj]:
                engine.add_obj(key)
            Rocket.debuginit += 1

        return False
