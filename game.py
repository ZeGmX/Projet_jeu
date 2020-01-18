import turtle, time
import shapes, bad_guys, rockets, game, engine, bullets


class Game:
    LENGTH = 640 #size of the window
    level = [[[] for _ in range(5)] for _ in range(3)]
    posi = 0
    posj = 4
    pause = False
    ground = ""
    rocket = ""
    boss = ""

    def init_rockets():
        assert Game.rocket == "", "rocket already initialized"
        print("Initializing the rocket...")
        Game.rocket = rockets.Rocket()

    def init_ground():
        assert Game.ground == "", "ground already initialized"
        print("Initializing the ground...")
        Game.ground = shapes.Ground(Game.level[Game.posi][Game.posj])


    def init_boss():
        assert Game.boss == "", "boss already initialized"
        print("Initializing the Boss...")
        Game.boss = bad_guys.Boss(30, 0)






def gameplay(self):
    shapes.Key.pickupkey(0, 4, 0, 0, 4, -268, 0)
    shapes.Door.dooropening(0, 4, 1, 0, -300, 0, 0, 10)
    shapes.Key.pickupkey(1, 4, 1, 1, 2, -268, 0)
    shapes.Door.dooropening(1, 2, 2, 1, -300, 0, 0, 10)
    shapes.Key.pickupkey(0, 0, 2, 1, 1, 0, 268)
    shapes.Door.dooropening(1, 1, 3, 2, 0, 300, 10, 0)
    shapes.Key.pickupkey(0, 1, 3, 2, 2, 268, 0)
    shapes.Door.dooropening(2, 2, 4, 3, 300, 0, 0, 10)

    if bad_guys.Boss.bossbeaten == 1:
        if shapes.Door.ldoor[2][3] != []:
            (door, x, y) = shapes.Door.ldoor[2][3][0]
            key = shapes.Key.lkey[2][3][0]
            if door.y < 400:
                door.y += 10
                key.y += 10
            else:
                engine.del_obj(door)
                engine.del_obj(key)
                shapes.Door.ldoor[2][3].remove((door, x, y))
                shapes.Key.lkey[2][3].remove(key)

    if Game.posi == 2 and Game.posj == 4:
        banner('You won!')
        engine.exit_engine()





def load():
    engine.del_obj(Game.ground)
    Game.ground = shapes.Ground(Game.level[Game.posi][Game.posj])
    for i in range(3):
        for j in range(5):
            if i != Game.posi or j != Game.posj:
                for (door, _, _) in shapes.Door.ldoor[i][j]:
                    engine.del_obj(door)
                for key in shapes.Key.lkey[i][j]:
                    engine.del_obj(key)
                for badguy in bad_guys.BadGuy.badguys[i][j]:
                    engine.del_obj(badguy)
    for bullet in bullets.bullets:
        engine.del_obj(bullet)
    bullets.bullets = []

    #for _ in range(3):
    for badguy in bad_guys.BadGuy.badguys[Game.posi][Game.posj]:
        engine.add_obj(badguy)
    for (door , _, _) in shapes.Door.ldoor[Game.posi][Game.posj]:
        engine.add_obj(door)
    for key in shapes.Key.lkey[Game.posi][Game.posj]:
        engine.add_obj(key)



    if Game.posi == 2 and Game.posj == 3 and bad_guys.Boss.bossbeaten == 0 and Game.boss.life > 0 and bad_guys.Boss.bosshere < 2:
        engine.add_obj(Game.boss)
        bad_guys.Boss.bosshere += 1
    if (Game.posi != 2 or Game.posj != 3)  and bad_guys.Boss.bossbeaten == 0:
        bad_guys.Boss.bosshere = 0


def banner(msg):
    turtle.home()
    turtle.color('darkblue')
    turtle.write(msg, True, align='center', font=('Arial', 48, 'italic'))
    time.sleep(1)
    turtle.undo()
