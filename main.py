# A nice game.Game

### Importations ###
import turtle
import engine, bullets, bad_guys, rockets, shapes, game

### Functions ###



def keyboard_cb(key):
    "Gestion du clavier"

    if key == 'Return': #Enter
        game.Game.pause = not game.Game.pause
    if key == 'Escape':
        engine.exit_engine()
    if not game.Game.pause:
        if key == 'Up' or key == 'z':
            game.Game.rocket.rocket_up()
        if key == 'Left' or key == 'q':
            game.Game.rocket.rocket_left()
        if key == 'Right' or key == 'd':
            game.Game.rocket.rocket_right()
        if key == 'space':
            engine.add_obj(bullets.Bullet(game.Game.rocket.x, game.Game.rocket.y, 90 + game.Game.rocket.angle, True))



if __name__ == '__main__':

    turtle.hideturtle() #These three lines are hiding the drawing at the begining
    turtle.penup()
    turtle.speed("fastest")

    shapes.makeshape()

    game.Game.init_rockets()
    game.Game.init_ground()
    game.Game.init_boss()

    engine.init_screen(game.Game.LENGTH, game.Game.LENGTH)
    engine.init_engine()

    shapes.create_doors_keys()
    bad_guys.BadGuy.create_badguys()

    engine.add_obj(game.Game.ground)
    engine.add_obj(game.Game.rocket)

    engine.set_keyboard_handler(keyboard_cb)
    game.load()
    engine.engine()
