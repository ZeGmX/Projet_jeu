import turtle
import game, engine

class Menu:
    skin_list = []
    cursor_position = 0 #0: level, 1:tutorial, 2:skin, 3:exit
    select_arrow = ""

    def load_main_menu():
        print("Loading the main menu...")
        turtle.setpos(0, 210)
        turtle.write("Name of the game", align="center", font=("Arial", 55, "normal"))
        turtle.setpos(-50, 50)
        turtle.write("Choose a level", font=("Arial", 25, "normal"))
        turtle.setpos(-50, 0)
        turtle.write("Tutorial", font=("Arial", 25, "normal"))
        turtle.setpos(-50, -50)
        turtle.write("Choose a skin", font=("Arial", 25, "normal"))
        turtle.setpos(-50, -100)
        turtle.write("Quit game", font=("Arial", 25, "normal"))

        engine.set_keyboard_handler(Menu.keyboard_cb)
        assert Menu.select_arrow == "", "Select arrow already initialized"
        Menu.select_arrow = engine.GameObject(-80, 70, 0, 0, "select_arrow", "red")
        engine.add_obj(Menu.select_arrow)
        engine.engine()



    def keyboard_cb(key):
        "keyboard manager"
        if key == "Return": #enter
            if Menu.cursor_position == 0:
                engine.init_engine()
                game.Game.init_all()

                engine.add_obj(game.Game.ground)
                engine.add_obj(game.Game.rocket)

                game.cheat()
                engine.set_keyboard_handler(game.keyboard_cb)
                game.load()
            elif Menu.cursor_position == 3:
                engine.exit_engine()
            else:
                print("Feature not implemented yet")
        elif key == "Up":
            Menu.cursor_position = (Menu.cursor_position - 1) % 4
            Menu.select_arrow.y = 70 - 50 * Menu.cursor_position
        elif key == "Down":
            Menu.cursor_position = (Menu.cursor_position + 1) % 4
            Menu.select_arrow.y = 70 - 50 * Menu.cursor_position
