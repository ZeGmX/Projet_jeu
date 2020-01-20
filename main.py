# A nice game.Game

### Importations ###
import turtle, sys
import engine, bullets, bad_guys, rockets, shapes, game

### Functions ###



def keyboard_cb(key):
    "Gestion du clavier"
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
    "Pour un debug plus simple"
    if len(sys.argv) > 1 and sys.argv[1] == '0':
        print("Version avec cheat")
        key_order = [(0, 4), (1, 4), (0, 0), (0, 1), (2, 3)]
        door_order = [(0, 4), (1, 2), (1, 1), (2, 2), (2, 3)]
        game.Game.posi = 0
        game.Game.posj = 4
        game.Game.rocket.x = 0
        game.Game.rocket.y = 0
        shapes.Door.doorsopened = 0
        shapes.Key.pickedupkeys = list(range(1))
        bad_guys.Boss.bossbeaten = False

        for door_index in range(shapes.Door.doorsopened):
            i, j = door_order[door_index]
            door= shapes.Door.ldoor[i][j][0]
            engine.del_obj(door)
            shapes.Door.ldoor[i][j].remove(door)
        """
        for key_index in range(len(shapes.Key.pickedupkeys)):
            i, j = key_order[key_index]
            key = shapes.Key.lkey[i][j][0]
            shapes.Key.lkey[i][j].remove(key)
            if key_index == shapes.Key.pickedupkeys - 1 == shapes.Door.doorsopened:
                newi, newj = door_order[shapes.Key.pickedupkeys - 1]
                shapes.Key.lkey[newi][newj].append(key)
            else:
                engine.del_obj(key)""" # TODO ?
    else:
        print("Version sans cheat")


if __name__ == '__main__':

    turtle.hideturtle() #These three lines are hiding the drawing at the begining
    turtle.penup()
    turtle.speed("fastest")


    game.Game.init_game()
    shapes.makeshape()
    game.Game.init_rockets()
    game.Game.init_ground()
    game.Game.init_boss()

    engine.init_screen(game.Game.LENGTH, game.Game.LENGTH)
    engine.init_engine()

    shapes.Door.init_doors()
    shapes.Key.init_keys()
    bad_guys.BadGuy.create_badguys()

    engine.add_obj(game.Game.ground)
    engine.add_obj(game.Game.rocket)

    cheat()
    engine.set_keyboard_handler(keyboard_cb)
    game.load()
    engine.engine()
