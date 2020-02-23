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
    MAX_NB_LVL_PER_PAGE = min(10, len(listdir("Files/lvls/")) + 1)
    LINE_HEIGHT = 50
    LEVEL_LINE_HEIGHT = 0.08 * game.Game.LENGTH #to have the list cover 80% of the height
    FONT_SIZE = LINE_HEIGHT // 2
    SKIN_WINDOW_HEIGHT = game.Game.LENGTH / 2
    select_arrow = ""
    current_skin = ""
    current_skin_powered = ""
    skin_rect = ""
    lvl_rect = ""


    def load_main_menu():
        print("Loading the main menu...")
        pos_arrow = - game.Game.LENGTH / 5, game.Game.LENGTH / 9
        pos_title = 0, game.Game.LENGTH / 3
        x0, y0 = pos_arrow[0] + 40 , pos_arrow[1] - Menu.LINE_HEIGHT / 2 + 5 #+ 5 to have the arrow and the text aligned
        font_size_title = 55

        engine.set_keyboard_handler(Menu.keyboard_main)
        assert Menu.select_arrow == "", "Select arrow already initialized"
        Menu.select_arrow = engine.GameObject(*pos_arrow, 0, 0, "select_arrow", "black")
        engine.add_obj(Menu.select_arrow)
        Menu.cursor_position = 0

        turtle.clear()
        turtle.setpos(*pos_title)   #options to select
        turtle.write("Name of the game", align="center", font=("Arial", font_size_title, "normal"))
        str_list = ["Choose a level", "Tutorial", "Choose a skin", "Quit game"]
        for i in range(len(str_list)):
            turtle.setpos(x0, y0 - i * Menu.LINE_HEIGHT)
            turtle.write(str_list[i], font=("Arial", Menu.FONT_SIZE, "normal"))

        if not Menu.engine_launched:
            Menu.engine_launched = True
            engine.engine()

    def load_skin_selection_menu():
        print("Loading the skin selection menu...")
        x_arrow, y_arrow = game.Game.LENGTH / 3.5, - game.Game.LENGTH / 6
        arrow_height, arrow_width = 34.6, 30
        rect_txt_p1 = - (y_arrow + arrow_height / 2), - x_arrow + arrow_width / 2
        rect_txt_p2 = - (y_arrow - arrow_height / 2), x_arrow - arrow_width / 2
        rect_window_p1 = rect_txt_p1[0] - 20, rect_txt_p1[1] #20 : shift between the two rectangles
        rect_window_p2 = rect_txt_p1[0] - 20 - Menu.SKIN_WINDOW_HEIGHT, rect_txt_p2[1]

        engine.init_engine()
        engine.set_keyboard_handler(Menu.keyboard_skin)
        _ = engine.GameObject(x_arrow, y_arrow, 0, 0, "arrow_right_skin", "gray", True)
        _ = engine.GameObject(- x_arrow, y_arrow, 0, 0, "arrow_left_skin", "gray", True)
        _ = shapes.Rectangle(rect_window_p1, rect_window_p2)
        Menu.skin_rect = shapes.Rectangle(rect_txt_p1, rect_txt_p2)
        Menu.display_skin()

    def load_level_selection_menu():
        print("Loading the level selection menu...")
        pos_arrow = - game.Game.LENGTH // 5, 3 * Menu.LEVEL_LINE_HEIGHT + Menu.FONT_SIZE
        rect_p1 = game.Game.LENGTH // 2, game.Game.LENGTH // 2
        rect_p2 = - game.Game.LENGTH // 2, - game.Game.LENGTH // 2

        engine.init_engine()
        engine.set_keyboard_handler(Menu.keyboard_lvl)
        Menu.cursor_position = Menu.cursor_position_on_screen = 1
        assert Menu.select_arrow == "", "Select arrow already initialized"
        Menu.lvl_rect = shapes.Rectangle(rect_p1, rect_p2, color_edge="white")
        Menu.select_arrow = engine.GameObject(*pos_arrow, 0, 0, "select_arrow", "black")
        engine.add_obj(Menu.select_arrow)
        Menu.display_level()

    def keyboard_main(key):
        "keyboard manager for the main menu"
        y0 = game.Game.LENGTH / 9

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

        else:
            if key == "Up":
                Menu.cursor_position = (Menu.cursor_position - 1) % 4
            elif key == "Down":
                Menu.cursor_position = (Menu.cursor_position + 1) % 4
            Menu.select_arrow.y = y0 - Menu.LINE_HEIGHT * Menu.cursor_position

    def display_skin():
        y_arrow = - game.Game.LENGTH / 6
        arrow_height = 34.6
        y0 = y_arrow + arrow_height / 2 + 20
        r = Menu.skin_radius_list[Menu.skin_cursor]
        pos_skin_unpowered = 0, y0 + (Menu.SKIN_WINDOW_HEIGHT - r) / 3
        pos_skin_powered = 0, pos_skin_unpowered[1] + (Menu.SKIN_WINDOW_HEIGHT + 2 * r) / 3
        font_size = 15
        txt_pos = 0, y_arrow - font_size / 2 - 5

        if Menu.current_skin != "":
            engine.del_obj(Menu.current_skin)
            engine.del_obj(Menu.current_skin_powered)
        Menu.current_skin = engine.GameObject(*pos_skin_unpowered, 0, 0, Menu.skin_list[Menu.skin_cursor], "white", True)
        Menu.current_skin_powered = engine.GameObject(*pos_skin_powered, 0, 0, Menu.skin_list[Menu.skin_cursor] + "_powered", "white", True)
        Menu.current_skin.angle = 90
        Menu.current_skin_powered.angle = 180
        engine.add_obj(Menu.current_skin)
        Menu.skin_rect.draw()
        turtle.setpos(*txt_pos)
        turtle.pencolor("black")
        turtle.write(Menu.skin_list[Menu.skin_cursor], align="center", font=("Arial", font_size, "normal"))


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
            engine.del_obj(Menu.skin_rect)
            Menu.current_skin = Menu.current_skin_powered = Menu.skin_rect = ""
            Menu.load_main_menu()

    def display_level():
        nb_lvls = len(listdir("Files/lvls/"))
        str_list = ["Main Menu"] + [f"Level {i + 1}" for i in range(nb_lvls)]
        first_display_index = Menu.cursor_position - Menu.cursor_position_on_screen
        x0, y0 = - game.Game.LENGTH // 5 + 40 , 4 * Menu.LEVEL_LINE_HEIGHT + 5 #+5 to align the arrow and the text

        Menu.lvl_rect.draw()
        turtle.pencolor("black")
        for i in range(Menu.MAX_NB_LVL_PER_PAGE):
            turtle.setpos(x0, y0 - Menu.LEVEL_LINE_HEIGHT * i)
            turtle.write(str_list[first_display_index + i], font=("Arial", Menu.FONT_SIZE, "normal"))

    def keyboard_lvl(key):
        "keyboard manager for the level selection menu"
        total_lvl_number = len(listdir("Files/lvls/"))
        y0 = 4 * Menu.LEVEL_LINE_HEIGHT + Menu.FONT_SIZE

        if key == "Up":
            if Menu.cursor_position_on_screen > 0:
                Menu.cursor_position_on_screen -= 1
            elif Menu.cursor_position == 0: # and Menu.cursor_position_on_screen == 0
                Menu.cursor_position_on_screen = Menu.MAX_NB_LVL_PER_PAGE - 1
            #in other cases, the arrow remains on the top
            Menu.cursor_position = (Menu.cursor_position - 1) % (total_lvl_number + 1) # + 1 for the return button
            Menu.select_arrow.y = y0 - Menu.LEVEL_LINE_HEIGHT * Menu.cursor_position_on_screen
            Menu.display_level()

        if key == "Down":
            if Menu.cursor_position_on_screen < Menu.MAX_NB_LVL_PER_PAGE - 1:
                Menu.cursor_position_on_screen += 1
            elif Menu.cursor_position == total_lvl_number: # and Menu.cursor_position_on_screen == MAX_NB_LVL_PER_PAGE - 1
                Menu.cursor_position_on_screen = 0
            #in other cases, the arrow remains on the bottom
            Menu.cursor_position = (Menu.cursor_position + 1) % (total_lvl_number + 1) # + 1 for the return button
            Menu.select_arrow.y = y0 - Menu.LEVEL_LINE_HEIGHT * Menu.cursor_position_on_screen
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
