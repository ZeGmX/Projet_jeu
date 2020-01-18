import math
import engine, game, bad_guys, shapes

bullets = []


class Bullet(engine.GameObject):
    "Bullets shot by ennemies"

    def __init__(self, x, y, angle, nice):
        self.angle = angle
        self.speed = 3
        self.radius = 5
        self.nice = nice #to know if it was fired by the player of a bad guy
        bullets.append(self)
        super().__init__(x, y, 0, 0, 'graybullet', 'black')

    def move(self):
        if not game.Game.pause:
            self.x += self.speed * math.cos(math.radians(180 - self.angle))
            self.y -= self.speed * math.sin(math.radians(180 - self.angle))


            if self.nice:
                for badguy in bad_guys.BadGuy.badguys[game.Game.posi][game.Game.posj]: #collision with a bad_guy
                    if shapes.collide_round_round(self, badguy):
                        engine.del_obj(badguy)
                        bad_guys.BadGuy.badguys[game.Game.posi][game.Game.posj].remove(badguy)
                        self.shape = 'whitebullet'
                        engine.del_obj(self)
                        bullets.remove(self)

                if game.Game.posi == 2 and game.Game.posj == 3 and shapes.collide_round_round(self, game.Game.boss) and not game.Game.boss.bossbeaten:
                    self.shape = 'whitebullet'
                    engine.del_obj(self)
                    bullets.remove(self)
                    if bad_guys.Boss.bossbeaten == 0 and game.Game.boss.life == 0:
                        engine.del_obj(game.Game.boss)
                        game.banner('Boss defeated')
                        bad_guys.Boss.bossbeaten = 1
                    game.Game.boss.life -= 1



            elif shapes.collide_round_round(self, game.Game.rocket): #bad bullets collides with the rocket
                game.Game.rocket.losealife()
                self.shape = 'whitebullet'
                engine.del_obj(self)


            if shapes.collide_gnd(self):
                self.shape = 'whitebullet'
                engine.del_obj(self)
                bullets.remove(self)
