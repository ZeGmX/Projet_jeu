import turtle, time
import shapes, bad_guys, rockets, game, engine, bullets


class Game:
    LENGTH = 640 #size of the window

    level = [] #these will be initialized using the file Files/lvl{i}/lvl.txt
    posi = 0
    posj = 0
    length = 0
    height = 0

    pause = False #these have no other initilization
    freeze_spawn = True

    ground = "" #these have their own initialization function
    rocket = ""
    boss = ""

    def init_game(level="lvl1"):
        with open("Files/" + level + "/lvl.txt", 'r') as f:
            lines = f.readlines()
            assert len(lines) == 3, "Unconsistent file: Files" + level + "/lvl.txt"
            line_length = lines[0].split()
            line_height = lines[1].split()
            line_spawn = lines[2].split()
            Game.length = int(line_length[1])
            Game.height = int(line_height[1])
            Game.level = [[[] for _ in range(Game.length)] for _ in range(Game.height)]
            Game.posi = int(line_spawn[1])
            Game.posj = int(line_spawn[2])

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


class Stats:
    POINTS_PER_BAD_GUY = 100
    POINTS_PER_HIT_BOSS = 20
    POINTS_PER_KEY_PICKED = 50
    POINTS_PER_DOOR_OPENED = 50
    t_init = time.time()
    t_end = 0
    bullets_fired = 0
    bullets_hit = 0
    key_pressed = 0
    points = 0

    def display_stats():
        Stats.t_end = time.time()
        dt = int(Stats.t_end - Stats.t_init)
        hours = dt // 3600
        dt = dt % 3600
        mins = dt // 60
        seconds = dt % 60
        print("**********Statistics**********")
        print(f"Points : {Stats.points}")
        print(f"Time played : {hours}h {mins}min {seconds}s")
        print(f"Bullets fired : {Stats.bullets_fired}")
        print(f"Buletts hit : {Stats.bullets_hit}")
        print("Accuracy : {}%".format(Stats.bullets_hit / Stats.bullets_fired * 100 if Stats.bullets_fired > 0 else "NaN"))
        print(f"Number of keys pressed : {Stats.key_pressed}")
        print(f"Lives left : {Game.rocket.lives}")
        print(f"Keys picked : {len(shapes.Key.pickedupkeys)}")
        print(f"Doors opened : {shapes.Door.doorsopened}")
        print("*" * 30)


def gameplay(self):
    for door in shapes.Door.ldoor[Game.posi][Game.posj]:
        door.dooropening()
    for key in shapes.Key.lkey[Game.posi][Game.posj]:
        key.pickupkey()
    """shapes.Key.pickupkey(0, 4, 0, 0, 4, -268, 0)
    shapes.Door.dooropening(0, 4, 1, 0, -300, 0)
    shapes.Key.pickupkey(1, 4, 1, 1, 2, -268, 0)
    shapes.Door.dooropening(1, 2, 2, 1, -300, 0)
    shapes.Key.pickupkey(0, 0, 2, 1, 1, 0, 268)
    shapes.Door.dooropening(1, 1, 3, 2, 0, 300)
    shapes.Key.pickupkey(0, 1, 3, 2, 2, 268, 0)
    shapes.Door.dooropening(2, 2, 4, 3, 300, 0)"""

    if bad_guys.Boss.bossbeaten == 1:
        if shapes.Door.ldoor[2][3] != []:
            door = shapes.Door.ldoor[2][3][0]
            key = shapes.Key.lkey[2][3][0]
            if door.y < 400:
                door.y += 10
                key.y += 10
            else:
                engine.del_obj(door)
                engine.del_obj(key)
                shapes.Door.ldoor[2][3].remove(door)
                shapes.Key.lkey[2][3].remove(key)

    if Game.posi == 2 and Game.posj == 4:
        banner('You won!')
        engine.exit_engine()
        Stats.display_stats()



def load():
    engine.del_obj(Game.ground)
    Game.ground = shapes.Ground(Game.level[Game.posi][Game.posj])
    for i in range(3):
        for j in range(5):
            if i != Game.posi or j != Game.posj:
                for door in shapes.Door.ldoor[i][j]:
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
    for door in shapes.Door.ldoor[Game.posi][Game.posj]:
        engine.add_obj(door)
    for key in shapes.Key.lkey[Game.posi][Game.posj]:
        engine.add_obj(key)

    if Game.posi == 2 and Game.posj == 3 and not bad_guys.Boss.bossbeaten and Game.boss.life > 0:
        engine.add_obj(Game.boss)



def banner(msg):
    turtle.home()
    turtle.color('darkblue')
    turtle.write(msg, True, align='center', font=('Arial', 48, 'italic'))
    time.sleep(1)
    turtle.undo()
