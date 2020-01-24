import math
import engine, game, bad_guys, shapes



class Bullet(engine.GameObject):
    bullet_list = []

    def __init__(self, x, y, angle, nice):
        self.angle = angle
        self.speed = 3
        self.radius = 5
        self.nice = nice #to know if it was fired by the player of a bad guy
        self.pt_coll = Bullet.collision_point(x, y, angle)
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

            #if shapes.collide_gnd(self) or shapes.collide_door(self):
            if math.sqrt((self.x - self.pt_coll[0]) ** 2 + (self.y - self.pt_coll[1]) ** 2) <= self.radius or shapes.collide_door(self):
                self.hit()

    def hit(self, earn_points=False):
        "invoked when a bullet hits something and should be removed"
        self.shape = 'whitebullet'
        engine.del_obj(self)
        Bullet.bullet_list.remove(self)
        if earn_points:
            game.Stats.bullets_hit += 1
            game.Stats.points += game.Stats.POINTS_PER_BAD_GUY

    def fire_at_rocket(enemy):
        "launches a bullet at the rocket"
        angle_to_be_added = 0   #Computing the direction to fire the bullet
        if enemy.x < game.Game.rocket.x:
            angle_to_be_added = 180
        if enemy.x == game.Game.rocket.x:
            angle = 0
        else:
            angle = angle_to_be_added +  math.degrees(math.atan((enemy.y - game.Game.rocket.y) / (enemy.x - game.Game.rocket.x)))
        engine.add_obj(Bullet(enemy.x, enemy.y, angle, False))

    def collision_point(x, y, angle):
        "Computing the collision point of the bullet \
        assuming that it goes in a straight line"
        ap = 1 #apy +bpx +cp = 0 for the trajectory
        bp = math.tan(math.radians(180 - angle))
        cp = - ap * y - bp * x
        collision_pt = (game.Game.LENGTH, game.Game.LENGTH)
        dist_collision = math.sqrt((collision_pt[0] - x) ** 2 + (collision_pt[1] - y) ** 2)
        for poly in game.Game.level[game.Game.posi][game.Game.posj]:
            for i in range(len(poly)):
                x1, y1 = poly[i - 1]
                x2, y2 = poly[i]
                a = x2 - x1
                b = y1 - y2 #ay + bx + c = 0 for this segment
                c = - a * y2 - b * x2
                det = a * bp - b * ap
                """determinant of the matrix [a b] = A
                                             [ap bp]
                we can find the intersection by solving the system A [y x] = [-c  -cp]"""
                if abs(det) <= 1e-5:
                    pass
                else:
                    newy = (- c * bp + cp * b) / det
                    newx = (- a * cp + ap * c) / det
                    newdist = math.sqrt((newx - x) ** 2 + (newy - y) ** 2)
                    if newdist < dist_collision: #Closer than the last point
                        angle_360 = angle % 360
                        if (angle_360 <= 180 and newy <= y) or \
                                (angle_360 >= 180 and newy >= y): #splitting horizontally
                            if ((angle_360 <= 90 or angle_360 >= 270) and newx <= x) \
                                    or (90 <= angle_360 <= 270 and newx >= x): #splitting vertically
                                if min(x1, x2) <= newx <= max(x1, x2) and min(y1, y2) <= newy <= max(y1, y2): #checking if the point is on the segment
                                    collision_pt = (newx, newy)
                                    dist_collision = newdist
        return collision_pt
