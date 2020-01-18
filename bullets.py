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

        self.x += self.speed * math.cos(math.radians(180 - self.angle))
        self.y -= self.speed * math.sin(math.radians(180 - self.angle))

        for badguy in bad_guys.BadGuy.badguys[game.Game.posi][game.Game.posj] :
            if shapes.collide_round_round(self, badguy) :
                engine.del_obj(badguy)
                bad_guys.BadGuy.badguys[game.Game.posi][game.Game.posj].remove(badguy)
                self.shape = 'whitebullet'
                engine.del_obj(self)
                bullets.remove(self)

        if game.Game.posi == 2 and game.Game.posj == 3 and shapes.collide_round_round(self, game.Game.boss):
            self.shape = 'whitebullet'
            engine.del_obj(self)
            bullets.remove(self)
            if bad_guys.Boss.bossbeaten == 0:
                engine.del_obj(game.Game.boss)
                game.banner('Boss defeated')
                bad_guys.Boss.bossbeaten
            game.Game.boss.life -= 1

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

        if shapes.collide_round_round(self, game.Game.rocket) :
            game.Game.rocket.losealife()
            self.shape = 'whitebullet'
            engine.del_obj(self)


        if shapes.collide_gnd(self) :
            self.shape = 'whitebullet'
            engine.del_obj(self)
            bullets.remove(self)
