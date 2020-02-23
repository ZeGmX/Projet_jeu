import math, random
import engine, bullets, game


class BadGuy(engine.GameObject):
    badguys = [[[] for _ in range(5)] for _ in range(3)] #badguys in each room

    def __init__(self,x ,y):
        self.countdown = 0
        self.tresh = 150 # when countdown > tresh, it fires a bullet
        self.radius = 20
        super().__init__(x, y, 0, 0, 'badguy', 'black')

    def init_badguys(level="lvl1"):
        print("Initializing the enemies...")
        path = "Files/lvls/" + level + "/bad_guys.txt"
        with open(path, 'r') as f:
            lines = f.readlines()
            for line in lines[1:-1]: #line[-1] is for the boss
                split_line = line.split()
                posi, posj = int(split_line[0]), int(split_line[1])
                x, y = int(split_line[2]), int(split_line[3])
                BadGuy.badguys[posi][posj].append(BadGuy(x, y))

    def move(self):
        if not game.Game.pause:
            self.countdown += 1
            if self.countdown > self.tresh:
                self.countdown = 0
                bullets.Bullet.fire_at_rocket(self)


class Boss(engine.GameObject):
    bossbeaten = False

    def __init__(self, posi, posj, x ,y):
        self.countdown = 0
        self.tresh = 70
        self.life = 80
        self.radius = 100
        self.posi = posi
        self.posj = posj
        super().__init__(x, y, 0, 0, 'boss', 'black')
        engine.del_obj(self)

    def init_boss(level="lvl1"):
        assert game.Game.boss == "", "boss already initialized"
        print("Initializing the Boss...")
        path = "Files/lvls/" + level + "/bad_guys.txt"
        with open(path, 'r') as f:
            lines = f.readlines()
            boss_line = lines[-1].split()
            posi, posj = int(boss_line[0]), int(boss_line[1])
            x, y = int(boss_line[2]), int(boss_line[3])
            game.Game.boss = Boss(posi, posj, x, y)

    def move(self):
        if not game.Game.pause:
            self.countdown += 1
            if self.countdown > self.tresh:
                self.tresh = random.randrange(50, 70)
                self.countdown = 0
                bullets.Bullet.fire_at_rocket(self)
