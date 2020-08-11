# A nice game.Game
import turtle
import engine
from menu import Menu
import game
import shapes


if __name__ == '__main__':

    turtle.hideturtle()  # These three lines are hiding the drawing at the beginning
    turtle.penup()
    turtle.speed("fastest")

    engine.init_screen(game.Game.LENGTH, game.Game.LENGTH)
    engine.init_engine()

    shapes.makeshape()
    Menu.load_main_menu()
    """
    game.Game.init_all()

    engine.add_obj(game.Game.ground)
    engine.add_obj(game.Game.rocket)

    cheat()
    engine.set_keyboard_handler(keyboard_cb)
    game.load()
    engine.engine()"""
