import math
import engine, game, bad_guys, shapes

bullets = []


class NiceBullet(engine.GameObject) :
    "Bullets shot by the player"

    def __init__(self, x, y, angle) :
        self.angle = angle
        self.speed = 3
        self.radius = 5
        bullets.append(self)
        super().__init__(x, y, 0, 0, 'graybullet', 'black')

    def move(self) :

        #global bossbeaten

        self.x += self.speed * math.cos(math.radians(180 - self.angle))
        self.y -= self.speed * math.sin(math.radians(180 - self.angle))

        for badguy in bad_guys.BadGuy.badguys[game.posi][game.posj] :
            if shapes.collide_round_round(self, badguy) :
                engine.del_obj(badguy)
                bad_guys.BadGuy.badguys[game.posi][game.posj].remove(badguy)
                self.shape = 'whitebullet'
                engine.del_obj(self)
                bullets.remove(self)

        if game.posi == 2 and game.posj == 3 and shape.collide_round_round(self, boss):
            self.shape = 'whitebullet'
            engine.del_obj(self)
            bullets.remove(self)
            if boss.life > 0:
                boss.life -= 1
            elif bad_guys.Boss.bossbeaten == 0:
                engine.del_obj(boss)
                game.banner('Boss defeated')
                bad_guys.Boss.bossbeaten

        if shapes.collide_gnd(self) :
            self.shape = 'whitebullet'
            engine.del_obj(self)


class Bullet(engine.GameObject) :
    "Bullets shot by ennemies"

    def __init__(self, x, y, angle) :
        self.angle = angle
        self.speed = 3
        self.radius = 5
        bullets.append(self)
        super().__init__(x, y, 0, 0, 'graybullet', 'black')

    def move(self) :

        self.x += self.speed * math.cos(math.radians(180 - self.angle))
        self.y -= self.speed * math.sin(math.radians(180 - self.angle))

        if shapes.collide_round_round(self, game.rocket) :
            game.rocket.losealife()
            self.shape = 'whitebullet'
            engine.del_obj(self)


        if shapes.collide_gnd(self) :
            self.shape = 'whitebullet'
            engine.del_obj(self)
            bullets.remove(self)
