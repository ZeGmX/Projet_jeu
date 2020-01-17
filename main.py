# A nice game.Game

### Importations ###
import turtle
import engine, bullets, bad_guys, rockets, shapes, game

### Functions ###



def keyboard_cb(key):

    if key == 'Escape':
        engine.exit_engine()
    if key == 'Up':
        game.Game.rocket.rocket_up()
    if key == 'Left' :
        game.Game.rocket.rocket_left()
    if key == 'Right' :
        game.Game.rocket.rocket_right()
    if key == 'space' :
        engine.add_obj(bullets.NiceBullet(game.Game.rocket.x, game.Game.rocket.y, 90 + game.Game.rocket.angle))

"""
    if key == 'm':
        rocket.speed = 0
        rocket = Rocket()
        engine.add_obj(rocket)
"""







print(1)
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
