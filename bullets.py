import math
import engine, game, bad_guys, shapes



class Bullet(engine.GameObject):
    bullet_list = []

    def __init__(self, x, y, angle, nice):
        self.angle = angle
        self.speed = 3
        self.radius = 5
        self.nice = nice #to know if it was fired by the player of a bad guy
        Bullet.bullet_list.append(self)
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
                        self.hit(earn_points=True)

                if game.Game.posi == game.Game.boss.posi and game.Game.posj == game.Game.boss.posj and shapes.collide_round_round(self, game.Game.boss) and not game.Game.boss.bossbeaten:
                    self.hit(earn_points=True)
                    game.Game.boss.life -= 1
                    if game.Game.boss.life == 0:
                        engine.del_obj(game.Game.boss)
                        game.banner('Boss defeated')
                        bad_guys.Boss.bossbeaten = True

            elif shapes.collide_round_round(self, game.Game.rocket): #bad bullets collides with the rocket
                self.hit()
                if not game.Game.rocket.bulletproof:
                    game.Game.rocket.losealife()

            if shapes.collide_gnd(self) or shapes.collide_door(self):
                self.hit()

    def hit(self, earn_points=False):
        self.shape = 'whitebullet'
        engine.del_obj(self)
        Bullet.bullet_list.remove(self)
        if earn_points:
            game.Stats.bullets_hit += 1
            game.Stats.points += game.Stats.POINTS_PER_BAD_GUY
