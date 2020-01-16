import engine
import bullets


class BadGuy(engine.GameObject) :
    badguys = [[[] for _ in range(5)] for _ in range(3)]

    def __init__(self,x ,y) :
        self.countdown = 0
        self.seuil = 150
        self.radius = 20
        super().__init__(x, y, 0, 0, 'badguy', 'black', True) #True because it is static

    def move(self) :
        self.countdown += 1
        if self.countdown > self.seuil :
            self.seuil = 150
            self.countdown = 0
            enplus = 0
            if self.x < game.rocket.x :
                enplus = 180
            if self.x == game.rocket.x :
                angle = 0
            else :
                angle = enplus +  math.degrees(math.atan((self.y - game.rocket.y) / (self.x - game.rocket.x)))
            engine.add_obj(bullets.Bullet(self.x, self.y, angle))

    def create_badguys():
        BadGuy.badguys[1][3].append(BadGuy(-270, -100))
        BadGuy.badguys[0][3].append(BadGuy(-95, 220))
        BadGuy.badguys[0][3].append(BadGuy(-95, -250))
        BadGuy.badguys[0][2].append(BadGuy(-295, 50))
        BadGuy.badguys[1][4].append(BadGuy(220, -220))
        BadGuy.badguys[1][4].append(BadGuy(-40, 220))
        BadGuy.badguys[1][0].append(BadGuy(-220, -160))
        BadGuy.badguys[1][1].append(BadGuy(-280, 180))
        BadGuy.badguys[0][0].append(BadGuy(40, 140))
        BadGuy.badguys[2][0].append(BadGuy(50, -220))
        BadGuy.badguys[2][0].append(BadGuy(-190, -190))
        BadGuy.badguys[2][2].append(BadGuy(90, 230))

class Boss(engine.GameObject) :
    bossbeaten = 0
    bosshere = 0

    def __init__(self,x ,y) :
        self.countdown = 0
        self.seuil = 70
        self.life = 80
        self.radius = 100
        super().__init__(x, y, 0, 0, 'boss', 'black', True) #True because it is static

    def move(self) :
        self.countdown += 1
        if self.countdown > self.seuil:
            self.seuil = random.randrange(50, 70)
            self.countdown = 0
            enplus = 0
            if self.x < game.rocket.x:
                enplus = 180
            if self.x == game.rocket.x:
                angle = 0
            else:
                angle = enplus +  math.degrees(math.atan((self.y - game.rocket.y) / (self.x - game.rocket.x)))
            engine.add_obj(Bullet(self.x, self.y, angle))
