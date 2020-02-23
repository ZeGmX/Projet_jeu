import turtle, time, sys
import shapes, bad_guys, rockets, game, engine, bullets


class Game:
    LENGTH = 640 #size of the window

    level = [] #these will be initialized using the file Files/lvl{i}/lvl.txt
    platforms = []
    posi = 0
    posj = 0
    length = 0
    height = 0
    win_posi = 0
    win_posj = 0

    pause = False #these have no other initilization
    freeze_spawn = True

    ground = "" #these have their own initialization function
    rocket = ""
    boss = ""

    def init_all(level="lvl1"):
        Game.init_game()
        #shapes.makeshape()
        rockets.Rocket.init_rockets()
        shapes.Ground.init_ground(level)
        shapes.Ground.init_platforms()
        bad_guys.Boss.init_boss(level)
        shapes.Door.init_doors(level)
        shapes.Key.init_keys(level)
        bad_guys.BadGuy.init_badguys(level)

    def init_game(level="lvl1"):
        path = "Files/lvls/" + level + "/lvl.txt"
        with open(path, 'r') as f:
            lines = f.readlines()
            assert len(lines) == 4, "Unconsistent file: " + path
            line_length = lines[0].split()
            line_height = lines[1].split()
            line_spawn = lines[2].split()
            line_win_zone = lines[3].split()
            Game.length, Game.height = int(line_length[1]), int(line_height[1])
            Game.level = [[[] for _ in range(Game.length)] for _ in range(Game.height)]
            Game.posi, Game.posj = int(line_spawn[1]), int(line_spawn[2])
            Game.win_posi, Game.win_posj = int(line_win_zone[1]), int(line_win_zone[2])







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
    last_time_registered = time.time() #for the FPS counter
    last_age_registered = 0

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

    def show_fps():
        if '1' in sys.argv:
            t = time.time()
            if t > Stats.last_time_registered + 1:
                age = Game.rocket.age
                print(f"FPS : {age - Stats.last_age_registered}")
                Stats.last_time_registered = t
                Stats.last_age_registered = age





def gameplay(self):
    for door in shapes.Door.ldoor[Game.posi][Game.posj]:
        door.dooropening()
    for key in shapes.Key.lkey[Game.posi][Game.posj]:
        key.pickupkey()

    if bad_guys.Boss.bossbeaten:
        if shapes.Door.ldoor[Game.boss.posi][Game.boss.posj] != []:
            door = shapes.Door.ldoor[Game.boss.posi][Game.boss.posj][0]
            key = shapes.Key.lkey[Game.boss.posi][Game.boss.posj][0]
            if door.y < 400:
                door.y += 10
                key.y += 10
            else:
                engine.del_obj(door)
                engine.del_obj(key)
                shapes.Door.ldoor[Game.boss.posi][Game.boss.posj].remove(door)
                shapes.Key.lkey[Game.boss.posi][Game.boss.posj].remove(key)

    if Game.posi == Game.win_posi and Game.posj == Game.win_posj:
        banner('You won!')
        engine.exit_engine()
        Stats.display_stats()



def load():
    for bullet in bullets.Bullet.bullet_list:
        engine.del_obj(bullet)
    bullets.Bullet.bullet_list = []

    engine.del_obj(Game.ground)
    Game.ground = shapes.Ground(Game.level[Game.posi][Game.posj])

    for i in range(Game.height):
        for j in range(Game.length):
            if i != Game.posi or j != Game.posj:
                for door in shapes.Door.ldoor[i][j]:
                    engine.del_obj(door)
                for key in shapes.Key.lkey[i][j]:
                    engine.del_obj(key)
                for badguy in bad_guys.BadGuy.badguys[i][j]:
                    engine.del_obj(badguy)

    #for _ in range(3):
    for badguy in bad_guys.BadGuy.badguys[Game.posi][Game.posj]:
        engine.add_obj(badguy)
        badguy.countdown = 0
    for door in shapes.Door.ldoor[Game.posi][Game.posj]:
        engine.add_obj(door)
    for key in shapes.Key.lkey[Game.posi][Game.posj]:
        engine.add_obj(key)

    if Game.posi == Game.boss.posi and Game.posj == Game.boss.posj and not bad_guys.Boss.bossbeaten:
        engine.add_obj(Game.boss)

def banner(msg):
    turtle.home()
    turtle.color('darkblue')
    turtle.write(msg, True, align='center', font=('Arial', 48, 'italic'))
    time.sleep(1)
    turtle.undo()

def keyboard_cb(key):
    "keybord manager"
    turtle.setx(0)
    turtle.sety(0)
    game.Stats.key_pressed += 1
    game.Game.freeze_spawn = False
    if key == 'Return': #Enter
        game.Game.pause = not game.Game.pause
    if key == 'Escape':
        engine.exit_engine()
        game.Stats.display_stats()
    if not game.Game.pause:
        if key == 'Up' or key == 'z':
            game.Game.rocket.rocket_up()
        if key == 'Left' or key == 'q':
            game.Game.rocket.rocket_left()
        if key == 'Right' or key == 'd':
            game.Game.rocket.rocket_right()
        if key == 'space':
            engine.add_obj(bullets.Bullet(game.Game.rocket.x, game.Game.rocket.y, 90 + game.Game.rocket.angle, True))
            game.Stats.bullets_fired += 1

def cheat():
    "For an easier debug"
    if '0' in sys.argv:
        print("Version avec cheat")
        key_order = [(0, 4), (1, 4), (0, 0), (0, 1), (2, 3)]
        door_order = [(0, 4), (1, 2), (1, 1), (2, 2), (2, 3)]
        game.Game.posi = 2
        game.Game.posj = 2
        game.Game.rocket.x = 0
        game.Game.rocket.y = 0
        shapes.Key.pickedupkeys = list(range(4))
        bad_guys.Boss.bossbeaten = False
        doors_opened = 1
        game.Game.rocket.bulletproof = True

        for door_index in range(doors_opened):
            i, j = door_order[door_index]
            door = shapes.Door.ldoor[i][j][0]
            engine.del_obj(door)
            shapes.Door.ldoor[i][j].remove(door)
        for key_index in shapes.Key.pickedupkeys:
            i, j = key_order[key_index]
            key = shapes.Key.lkey[i][j][0]
            shapes.Key.lkey[i][j].remove(key)
            if key_index >= doors_opened:
                key.x = key.newx
                key.y = key.newy
                shapes.Key.lkey[key.newi][key.newj].append(key)
            else:
                engine.del_obj(key)
    else:
        print("Version sans cheat")
