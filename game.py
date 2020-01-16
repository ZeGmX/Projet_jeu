# A nice game

### Importations ###
import turtle
import random
import math
import time
import engine, bullets, bad_guys, rockets, shapes


### Global variables ###
LENGTH = 640
level = [[[] for _ in range(5)] for _ in range(3)]
posi = 0
posj = 4
shapes.makeshape()
rocket = rockets.Rocket()
ground = shapes.Ground(level[posi][posj])






### Functions ###

def banner(msg):
    turtle.home()
    turtle.color('darkblue')
    turtle.write(msg, True, align='center', font=('Arial', 48, 'italic'))
    time.sleep(1)
    turtle.undo()

def keyboard_cb(key):
    if key == 'Escape':
        engine.exit_engine()
    if key == 'Up':
        rocket.rocket_up()
    if key == 'Left' :
        rocket.rocket_left()
    if key == 'Right' :
        rocket.rocket_right()
    if key == 'space' :
        engine.add_obj(NiceBullet(rocket.x, rocket.y, 90 + rocket.angle))

"""
    if key == 'm':
        rocket.speed = 0
        rocket = Rocket()
        engine.add_obj(rocket)
"""




def load():
    global ground
    engine.del_obj(ground)
    ground = shapes.Ground(level[posi][posj])
    for i in range(3):
        for j in range(5):
            if i != posi or j != posj:
                for (door, _, _) in shapes.Door.ldoor[i][j]:
                    engine.del_obj(door)
                for key in shapes.Key.lkey[i][j]:
                    engine.del_obj(key)
                for badguy in bad_guys.BadGuy.badguys[i][j]:
                    engine.del_obj(badguy)
    for bullet in bullets.bullets:
        engine.del_obj(bullet)
    bullets.bullets = []

    for _ in range(3):
        for badguy in bad_guys.BadGuy.badguys[posi][posj]:
            engine.add_obj(badguy)
        for (door , _, _) in shapes.Door.ldoor[posi][posj]:
            engine.add_obj(door)
        for key in shapes.Key.lkey[posi][posj]:
            engine.add_obj(key)



    if posi == 2 and posj == 3 and bad_guys.Boss.bossbeaten == 0 and boss.life > 0 and bad_guys.Boss.bosshere < 2:
        engine.add_obj(boss)
        bad_guys.Boss.bosshere += 1
    if (posi != 2 or posj != 3)  and bad_guys.Boss.bossbeaten == 0:
        bad_guys.Boss.bosshere = 0




def gameplay(self):
        #global pickedupkeys, doorsopened, lkey

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

        if posi == 2 and posj == 4:
            banner('You won!')
            engine.exit_engine()


if __name__ == '__main__':

    engine.init_screen(LENGTH, LENGTH)
    engine.init_engine()
    #shapes.makeshape()
    shapes.create_doors_keys()
    bad_guys.BadGuy.create_badguys()
    #rocket = rockets.Rocket()
    boss = bad_guys.Boss(30, 0)
    engine.del_obj(boss)
    #ground = shapes.Ground(level[posi][posj])
    engine.add_obj(ground)
    engine.add_obj(rocket)
    #badguys = [BadGuy(-100, 225)]
    #badguys = []
    engine.set_keyboard_handler(keyboard_cb)
    load()
    engine.engine()
