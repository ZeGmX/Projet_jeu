import turtle, time
import game, engine, rockets

class Menu:
    skin_list = []
    skin_radius_list = []
    cursor_position = 0 #0: level, 1:tutorial, 2:skin, 3:exit
    skin_cursor = 0
    engine_launched = False
    select_arrow = ""
    current_skin = ""
    current_skin_powered = ""
    arrow_left = ""
    arrow_right = ""


    def load_main_menu():
        print("Loading the main menu...")

        engine.set_keyboard_handler(Menu.keyboard_main)
        assert Menu.select_arrow == "", "Select arrow already initialized"
        Menu.select_arrow = engine.GameObject(-80, 70, 0, 0, "select_arrow", "black")
        engine.add_obj(Menu.select_arrow)

        turtle.clear()
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

        if not Menu.engine_launched:
            Menu.engine_launched = True
            engine.engine()

    def load_skin_selection():
        print("Loading the skin selection menu...")
        engine.init_engine()
        engine.set_keyboard_handler(Menu.keyboard_skin)
        Menu.arrow_right = engine.GameObject(170, -100, 0, 0, "arrow_right_skin", "gray", True)
        Menu.arrow_left = engine.GameObject(-170, -100, 0, 0, "arrow_left_skin", "gray", True)
        Menu.display_skin()

    def keyboard_main(key):
        "keyboard manager for the main menu"
        if key == "Return": #enter
            engine.del_obj(Menu.select_arrow)
            Menu.select_arrow = ""
            if Menu.cursor_position == 0:
                engine.init_engine()
                game.Game.init_all()

                engine.add_obj(game.Game.ground)
                engine.add_obj(game.Game.rocket)

                game.cheat()
                engine.set_keyboard_handler(game.keyboard_cb)
                game.load()
            elif Menu.cursor_position == 2:
                Menu.load_skin_selection()
            elif Menu.cursor_position == 3:
                engine.exit_engine()
            else:
                print("Feature not implemented yet")
                Menu.load_main_menu()
            Menu.cursor_position = 0
        elif key == "Up":
            Menu.cursor_position = (Menu.cursor_position - 1) % 4
            Menu.select_arrow.y = 70 - 50 * Menu.cursor_position
        elif key == "Down":
            Menu.cursor_position = (Menu.cursor_position + 1) % 4
            Menu.select_arrow.y = 70 - 50 * Menu.cursor_position

    def display_skin():
        if Menu.current_skin != "":
            engine.del_obj(Menu.current_skin)
            engine.del_obj(Menu.current_skin_powered)
        Menu.current_skin = engine.GameObject(0, 20, 0, 0, Menu.skin_list[Menu.skin_cursor], "white", True)
        Menu.current_skin_powered = engine.GameObject(0, 80, 0, 0, Menu.skin_list[Menu.skin_cursor] + "_powered", "white", True)
        Menu.current_skin.angle = 90
        Menu.current_skin_powered.angle = 180
        engine.add_obj(Menu.current_skin)


    def keyboard_skin(key):
        "keyboard manager for the skin selection"
        if key == "Right":
            Menu.skin_cursor = (Menu.skin_cursor + 1) % len(Menu.skin_list)
            Menu.display_skin()
        if key == "Left":
            Menu.skin_cursor = (Menu.skin_cursor - 1) % len(Menu.skin_list)
            Menu.display_skin()
        if key == "Return":
            rockets.Rocket.skin = Menu.skin_list[Menu.skin_cursor]
            rockets.Rocket.radius = Menu.skin_radius_list[Menu.skin_cursor]
            engine.del_obj(Menu.current_skin)
            engine.del_obj(Menu.current_skin_powered)
            engine.del_obj(Menu.arrow_right)
            engine.del_obj(Menu.arrow_left)
            Menu.current_skin = Menu.current_skin_powered = Menu.arrow_right = Menu.arrow_left = ""
            Menu.load_main_menu()
