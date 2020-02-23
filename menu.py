import turtle, time
import game, engine, rockets, shapes
from os import listdir

class Menu:
    skin_list = []
    skin_radius_list = []
    cursor_position = 0 #0: level, 1:tutorial, 2:skin, 3:exit for the main menu
    cursor_position_on_screen = 0 #may be different of cursor_position if there are more items thant what can be displayed on one page
    skin_cursor = 0
    engine_launched = False
    max_nb_lvl_per_page = min(10, len(listdir("Files/lvls/")) + 1)
    select_arrow = ""
    current_skin = ""
    current_skin_powered = ""
    skin_rect = ""
    lvl_rect = ""
    #arrow_left = ""
    #arrow_right = ""


    def load_main_menu():
        print("Loading the main menu...")

        engine.set_keyboard_handler(Menu.keyboard_main)
        assert Menu.select_arrow == "", "Select arrow already initialized"
        Menu.select_arrow = engine.GameObject(- game.Game.LENGTH // 5, 70, 0, 0, "select_arrow", "black")
        engine.add_obj(Menu.select_arrow)
        Menu.cursor_position = 0

        turtle.clear()
        turtle.setpos(0, 210)   #options to select
        turtle.write("Name of the game", align="center", font=("Arial", 55, "normal"))
        turtle.setpos(-100, 50)
        turtle.write("Choose a level", font=("Arial", 25, "normal"))
        turtle.setpos(-100, 0)
        turtle.write("Tutorial", font=("Arial", 25, "normal"))
        turtle.setpos(-100, -50)
        turtle.write("Choose a skin", font=("Arial", 25, "normal"))
        turtle.setpos(-100, -100)
        turtle.write("Quit game", font=("Arial", 25, "normal"))

        if not Menu.engine_launched:
            Menu.engine_launched = True
            engine.engine()

    def load_skin_selection_menu():
        print("Loading the skin selection menu...")
        engine.init_engine()
        engine.set_keyboard_handler(Menu.keyboard_skin)
        #Menu.arrow_right = engine.GameObject(170, -100, 0, 0, "arrow_right_skin", "gray", True)
        #Menu.arrow_left = engine.GameObject(-170, -100, 0, 0, "arrow_left_skin", "gray", True)
        x_arrow = game.Game.LENGTH / 3.76
        y_arrow = - game.Game.LENGTH / 6.4
        _ = engine.GameObject(x_arrow, y_arrow, 0, 0, "arrow_right_skin", "gray", True)
        _ = engine.GameObject(- x_arrow, y_arrow, 0, 0, "arrow_left_skin", "gray", True)
        _ = shapes.Rectangle((60, -150), (- x_arrow, 150))
        Menu.skin_rect = shapes.Rectangle((120, -150), (80, 150))
        Menu.display_skin()

    def load_level_selection_menu():
        print("Loading the level selection menu...")
        engine.init_engine()
        engine.set_keyboard_handler(Menu.keyboard_lvl)
        Menu.cursor_position = Menu.cursor_position_on_screen = 1
        assert Menu.select_arrow == "", "Select arrow already initialized"
        x_arrow = - game.Game.LENGTH // 5
        y_arrow = 175
        Menu.lvl_rect = shapes.Rectangle((game.Game.LENGTH // 2, game.Game.LENGTH // 2), (- game.Game.LENGTH, - game.Game.LENGTH), color_edge="white")
        Menu.select_arrow = engine.GameObject(x_arrow, y_arrow, 0, 0, "select_arrow", "black")
        Menu.display_level()
        engine.add_obj(Menu.select_arrow)
        #Add arrow, skin names

    def keyboard_main(key):
        "keyboard manager for the main menu"
        if key == "Return": #enter
            engine.del_obj(Menu.select_arrow)
            Menu.select_arrow = ""
            if Menu.cursor_position == 0:
                Menu.load_level_selection_menu()
            elif Menu.cursor_position == 2:
                Menu.load_skin_selection_menu()
            elif Menu.cursor_position == 3:
                engine.exit_engine()
            else:
                print("Feature not implemented yet")
                Menu.load_main_menu()
            #Menu.cursor_position = 0
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
        Menu.skin_rect.draw()
        turtle.setpos(0, -112)
        turtle.pencolor("black")
        turtle.write(Menu.skin_list[Menu.skin_cursor], align="center", font=("Arial", 15, "normal"))


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
            #engine.del_obj(Menu.arrow_right)
            #engine.del_obj(Menu.arrow_left)
            engine.del_obj(Menu.skin_rect)
            #Menu.current_skin = Menu.current_skin_powered = Menu.arrow_right = Menu.arrow_left = Menu.skin_rect = ""
            Menu.current_skin = Menu.current_skin_powered = Menu.skin_rect = ""
            Menu.load_main_menu()

    def display_level():
        nb_lvls = len(listdir("Files/lvls/"))
        str_list = ["Main Menu"] + [f"Level {i + 1}" for i in range(nb_lvls)]
        first_display_index = Menu.cursor_position - Menu.cursor_position_on_screen
        x0, y0 = - game.Game.LENGTH / 6.4 , 205
        Menu.lvl_rect.draw()
        turtle.pencolor("black")
        for i in range(Menu.max_nb_lvl_per_page):
            turtle.setpos(x0, y0 - 50 * i)
            turtle.write(str_list[first_display_index + i], font=("Arial", 25, "normal"))

    def keyboard_lvl(key):
        "keyboard manager for the level selection menu"
        total_lvl_number = len(listdir("Files/lvls/"))
        if key == "Up":
            if Menu.cursor_position_on_screen > 0:
                Menu.cursor_position_on_screen -= 1
                Menu.select_arrow.y += 50
            elif Menu.cursor_position == 0: # and Menu.cursor_position_on_screen == 0
                Menu.cursor_position_on_screen = Menu.max_nb_lvl_per_page - 1
                Menu.select_arrow.y = 225 - 50 * (Menu.max_nb_lvl_per_page - 1)
            #in other cases, the arrow remains on the top
            Menu.cursor_position = (Menu.cursor_position - 1) % (total_lvl_number + 1) # + 1 for the return button
            Menu.display_level()
        if key == "Down":
            if Menu.cursor_position_on_screen < Menu.max_nb_lvl_per_page - 1:
                Menu.cursor_position_on_screen += 1
                Menu.select_arrow.y -= 50
            elif Menu.cursor_position == total_lvl_number: # and Menu.cursor_position_on_screen == max_nb_lvl_per_page - 1
                Menu.cursor_position_on_screen = 0
                Menu.select_arrow.y = 225
            #in other cases, the arrow remains on the bottom
            Menu.cursor_position = (Menu.cursor_position + 1) % (total_lvl_number + 1) # + 1 for the return button
            Menu.display_level()
        if key == "Return":
            engine.del_obj(Menu.select_arrow)
            engine.del_obj(Menu.lvl_rect)
            Menu.select_arrow = Menu.lvl_rect = ""
            if Menu.cursor_position == 0:
                Menu.load_main_menu()
            else:
                lvl = "lvl" + str(Menu.cursor_position)

                engine.init_engine()
                game.Game.init_all(lvl)

                engine.add_obj(game.Game.ground)
                engine.add_obj(game.Game.rocket)

                game.cheat()
                engine.set_keyboard_handler(game.keyboard_cb)
                game.load()
