import turtle, math
import engine, game, rockets

class Ground(engine.GameObject):
    def __init__(self, compounds=[]):
        self.poly = compounds
        ground = turtle.Shape('compound')
        for poly in compounds:
            poly = tuple((-y, x) for (x, y) in poly)
            ground.addcomponent(poly, 'black')
        turtle.register_shape('ground', ground)
        super().__init__(0, 0, 0, 0, 'ground', 'black', True) #True beacause static objects


class Door(engine.GameObject):
    ldoor = []

    doorsopened = 0 # TO BE REMOVED - TODO

    def __init__(self, x, y, color, keys_required=[], angle=0):
        self.angle = angle
        self.x_init = x
        self.y_init = y
        self.keys_required = keys_required[:]
        super().__init__(x, y, 0, 0, 'door', color)
        engine.del_obj(self)

    def heading(self):
        return self.angle

    def dooropening(self, key_index=0, proximity=100):
        if not game.Game.pause and abs(game.Game.rocket.x - self.x_init) < proximity and abs(game.Game.rocket.y - self.y_init) < proximity:
            got_all_keys = True
            for key_id in self.keys_required:
                got_all_keys = got_all_keys and key_id in Key.pickedupkeys
            if got_all_keys:
                key = Key.lkey[game.Game.posi][game.Game.posj][key_index]
                xmvt = 0 if self.angle % 180 == 0 else 10
                ymvt = 10 if self.angle % 180 == 0 else 0
                if abs(self.x) < 400 and abs(self.y) < 400: #moving the door
                    self.x += xmvt
                    self.y += ymvt
                    key.x += xmvt
                    key.y += ymvt
                else:   #removing the door
                    Door.ldoor[game.Game.posi][game.Game.posj].remove(self)
                    engine.del_obj(self)
                    for key in Key.lkey[game.Game.posi][game.Game.posj]: #removing the keys used to open the door
                        if key.id in self.keys_required:
                            Key.lkey[game.Game.posi][game.Game.posj].remove(key)
                            engine.del_obj(key)
                    Door.doorsopened += 1
                    game.Stats.points += game.Stats.POINTS_PER_DOOR_OPENED

    def init_doors(level="lvl1"):
        print("Initializing the doors...")
        Door.ldoor = [[[] for _ in range(game.Game.length)] for _ in range(game.Game.height)]
        path = "Files/" + level + "/doors.txt"
        with open(path, 'r') as f:
            lines = f.readlines()
            Door.nb_doors = len(lines) - 1
            for line in lines[1:]:
                l = line.split()
                posi, posj = int(l[0]), int(l[1])
                x, y = int(l[2]), int(l[3])
                color = l[4]
                angle = int(l[5])
                keys_required = l[6].split(',')
                keys_required = [int(k) for k in keys_required]
                Door.ldoor[posi][posj].append(Door(x, y, color, keys_required, angle))



class Key(engine.GameObject):
    "Key for the doors"

    lkey = []

    pickedupkeys = []

    def __init__(self, x, y, color, key_id, newi, newj, newx, newy):
        self.key_id = key_id
        self.newi = newi #room after pickup
        self.newj = newj
        self.newx = newx #coordinates after pickup
        self.newy = newy
        super().__init__(x, y, 0, 0, 'key', color)
        engine.del_obj(self)

    def init_keys(level="lvl1"):
        print("Initializing the keys...")
        Key.lkey = [[[] for _ in range(game.Game.length)] for _ in range(game.Game.height)]
        path = "Files/" + level + "/keys.txt"
        with open(path, 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:
                l = line.split()
                posi, posj = int(l[0]), int(l[1])
                x, y = int(l[2]), int(l[3])
                color = l[4]
                key_id = int(l[5])
                newi, newj = int(l[6]), int(l[7])
                newx, newy = int(l[8]), int(l[9])
                Key.lkey[posi][posj].append(Key(x, y, color, key_id, newi, newj, newx, newy))

    def pickupkey(self):
        if game.Game.rocket.landed == True and self.key_id not in Key.pickedupkeys:
            Key.pickedupkeys.append(self.key_id)
            game.Stats.points += game.Stats.POINTS_PER_KEY_PICKED
            game.banner('Key collected')
            self.x = self.newx
            self.y = self.newy
            if self.newi != game.Game.posi or self.newj != game.Game.posj: #the door isn"t in the same room as the key
                Key.lkey[game.Game.posi][game.Game.posj].remove(self)
                Key.lkey[self.newi][self.newj].append(self)
                engine.del_obj(self)














def make_circle(point, radius):
    "draw a circle centerent on point"
    turtle.seth(90)
    turtle.setpos(point[0] + radius, point[1])
    turtle.begin_poly()
    turtle.circle(radius)
    turtle.end_poly()
    return turtle.get_poly()

def collide_round_round(round1, round2):
    "Checks if two round objects collide"
    if math.sqrt( (round1.x - round2.x) ** 2 + (round1.y - round2.y) ** 2) < round2.radius + round1.radius:
        return True

def collide_door(roundobj):
    "Checks if a round objects collides with a door"
    for door in Door.ldoor[game.Game.posi][game.Game.posj]:
        if door.x == 0 and abs(door.y - roundobj.y) < roundobj.radius + 40 and abs(door.x - roundobj.x) < 100 + roundobj.radius:    #40 = half width of the door, 100 = half height
            return True
        elif door.y == 0 and abs(door.x - roundobj.x) < roundobj.radius + 40 and abs(door.y - roundobj.y) < 100 + roundobj.radius:
            return True
    return False

def collide_round_poly(roundobj, poly):
    "Checks if a round object collides with a polygon"
    for i in range(len(poly)):
        x, y = game.Game.LENGTH, game.Game.LENGTH
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        if x1 == x2:
            x = x1
            y = roundobj.y
        elif y1 == y2 and abs(x2 - x1) != 80:
            x = roundobj.x
            y = y1
        elif y2 != y1:
            m = (y2 - y1) / (x2 - x1)
            p = y2 - m * x2
            pp = roundobj.y + roundobj.x / m
            x = (pp - p) / (m + 1 / m)
            y = m * x + p
        if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
            if math.sqrt((x - roundobj.x) ** 2 + (y - roundobj.y) ** 2) < roundobj.radius:
                return True
    return False

def collide_gnd(roundobj):
    "Checks if a round objects collides with the ground"
    res = False
    for poly in game.Game.ground.poly:
        res = res or collide_round_poly(roundobj, poly)
    return res

def makeshape():
    level = game.Game.level

    rocket = turtle.Shape("compound")
    body = ((15,0), (25.61, -10.61), (25.61, -55.61), (0, -34.5), (-25.61, -55.61), (-25.61, -10.61), (-15.5, 0))
    rocket.addcomponent(tuple((x, y + 27) for (x, y) in body), "white", "black")
    fire = ((0, -34.5), (3.35, -41.21), (0, -47.92), (-3.35, -41.21))
    rocket.addcomponent(tuple((x, y + 27) for (x, y) in fire), "orange", "orange")
    turtle.register_shape('rocket powered', rocket)

    rocket = turtle.Shape("compound")
    body = ((15,0), (25.61, -10.61), (25.61, -55.61), (0, -34.5), (-25.61, -55.61), (-25.61, -10.61), (-15.5, 0))
    rocket.addcomponent(tuple((x, y + 27) for (x, y) in body), "white", "black")
    turtle.register_shape('rocket', rocket)

    bullet = turtle.Shape('compound')
    bullet.addcomponent(make_circle((0, 0), 5), 'darkgray', 'darkgray')
    bullet.addcomponent(make_circle((-1,1), 3.59), 'lightgray', 'lightgray')
    turtle.register_shape('graybullet', bullet)

    bullet = turtle.Shape('compound')
    bullet.addcomponent(make_circle((0, 0), 5), 'white', 'white')
    turtle.register_shape('whitebullet', bullet)


    badguy = turtle.Shape('compound')
    badguy.addcomponent(make_circle((-2, 2), 20), 'red', 'red')
    badguy.addcomponent(make_circle((-5, 5), 10), 'pink', 'pink')
    turtle.register_shape('badguy', badguy)


    boss = turtle.Shape('compound')
    boss.addcomponent(make_circle((-2, 2), 100), 'red', 'red')
    boss.addcomponent(make_circle((-5, 5), 50), 'pink', 'pink')
    turtle.register_shape('boss', boss)

    body = make_circle((0, 0), 20)
    wing = make_circle((-15, 0), 20 / 3)
    eye = make_circle((12, 6), 20 / 3)
    eye2 = make_circle((15, 6), 2)
    mouth = ((6.37, -4.3), (21, -4.69), (19.5, -8.38), (4.66, -8.45), (2.95, -5.35), (2.82, -2.78), (5, 0), (18.76, -0.08), (21, -4.69), (6.37, -4.3))

    bird = turtle.Shape('compound')
    bird.addcomponent(body, 'yellow', 'black')
    bird.addcomponent(wing, 'white', 'black')
    bird.addcomponent(eye, 'white', 'black')
    bird.addcomponent(eye2, 'black', 'black')
    bird.addcomponent(mouth, 'orange', 'black')
    turtle.register_shape('bird', bird)

    bird = turtle.Shape('compound')
    bird.addcomponent(body, 'yellow', 'black')
    bird.addcomponent(wing, 'white', 'black')
    bird.addcomponent(eye, 'white', 'black')
    bird.addcomponent(eye2, 'black', 'black')
    bird.addcomponent(mouth, 'orange', 'black')
    bird.addcomponent(((-8,-22), (-8,-30)), 'black', 'black')
    bird.addcomponent(((-4,-22), (-4,-30)), 'black', 'black')
    bird.addcomponent(((0,-22), (0,-30)), 'black', 'black')
    bird.addcomponent(((8,-22), (8,-30)), 'black', 'black')
    bird.addcomponent(((4,-22), (4,-30)), 'black', 'black')
    turtle.register_shape('bird powered', bird)


    door = ((-25, 100), (25,100), (42, 58), (46, 13), (26, 13), (26, -13), (46, -13), (42, -58), (25, -100), (-25, -100), (-42, -58), (-46, -13), (-46, 13), (-42, 58))
    door = tuple((-y, x) for (x, y) in door)
    turtle.register_shape('door', door)

    key = ((-13, -13), (-13, 13), (13, 13), (13, -13))
    key = tuple((-y, x) for (x, y) in key)
    turtle.register_shape('key', key)

    poly = ((-250,-100), (-214,-194), (-137, -263), (-66, -210), (-26, -255), (39, -213), (72, -152), (152, -152), (236, -115), (261, -21), (228, 19), (272, 102), (263, 197), (200, 262), (113, 241), (79, 262), (30, 259), (-44, 223), (-137, 232), (-202, 261), (-232, 152), (-250, 100),  (-400, 100), (-400, 400), (400, 400), (400, -400), (-400, -400), (-400, -100))
    level[0][4].append(poly)

    poly = ((250, 100), (100, 243), (0, 200), (-21, 148), (-69, 228), (-183, 257), (-310, 185), (-400, 190), (-400, 400), (400, 400), (400, 100))
    level[0][3].append(poly)
    poly = ((250,-100), (200, -200), (179, -291), (200, -400), (400, -400), (400, -100))
    level[0][3].append(poly)
    poly = ((-48, -345), (-92, -263), (-181, -219), (-247, -116), (-382, -96), (-400, -400))
    level[0][3].append(poly)

    poly = ((350, 190), (280, 227), (184, 266), (118, 251), (-16, 227), (-69, 227), (-153, 248), (-200, 200), (-257, 116), (-307, 89), (-296, 26), (-233,-45), (-267, -114), (-200, -200), (-220, -400), (-400, -400), (-400, 400), (400, 400))
    level[0][2].append(poly)
    poly = ((87, -336), (131, -209), (224, -106), (354, -66), (400, -400))
    level[0][2].append(poly)

    poly = ((-350, 178), (-235, 240), (-119, 273), (-84, 145), (-19, 278), (99, 235), (186, 262), (280, 186), (302, 91), (222, 91), (178, 29), (272, -24), (283, -162), (202, -246), (29, -227), (-54, -270), (-320, -224), (-400, -400), (400, -400), (400, 400), (-400, 400))
    level[1][4].append(poly)

    poly = ((-320, 320), (-100, 320), (-100, 250), (-178, 277), (-215, 138), (-280, 200), (-297, 178), (-320, 97))
    level[1][1] .append(poly)
    poly = ((100, 320), (100, 250), (177, 256), (203, 175), (239, 196), (250, 100), (320, 100), (320, 320))
    level[1][1].append(poly)
    poly = ((320, -100), (320, -320), (-57, -320), (20, -223), (83, -241), (139, -164), (201, -179), (250, -100))
    level[1][1].append(poly)
    poly = ((-320, -130), (-278, -179), (-237, -261), (-320, -320))
    level[1][1].append(poly)

    poly = (-180,150), (-100, 150), (-59, 179), (21, 138), (0, 57), (-101, 41), (-119, -21), (-141, 0), (-200, 37), (-220, 117)
    level[0][1].append(poly)
    poly = (-100, -320), (-100, -250), (-199, -220), (-222, -162), (-279, -141), (-299, 15), (-278, 260), (-37, 317), (218, 278), (259, 158), (221, 20), (259, -41), (237, -119), (180, -183), (100, -250), (100, -320), (320, -320), (320, 320), (-320, 320), (-320, -320)
    level[0][1].append(poly)

    poly = ((320, -320), (-10, -320), (-81, -101), (-59, 96), (41, 120), (61, 178), (100, 100), (120, -63), (200, -63), (220, 57), (157, 258), (-81, 304), (-200, 200), (-241, -44), (-264, -320), (-320, -320), (-320, 320), (320, 320))
    level[0][0].append(poly)

    poly = ((-10, 320), (56, 196), (238, 180), (320, 97), (320, 320))
    level[1][0].append(poly)
    poly = ((320, -130), (302, -158), (223, -184), (162, -280), (140, -320), (320, -320))
    level[1][0].append(poly)
    poly = ((-100, -320), (-143, -203), (-219, -180), (-279, -43), (-280, 198), (-264, 320), (-320, 320), (-320, -320))
    level[1][0].append(poly)
    poly = ((-150, 100), (-70, 100), (62, 79), (45, 0), (-60, -43), (-78, -103), (-119, 0), (-201, 60))
    level[1][0].append(poly)

    poly = ((200, 350), (210, 300), (225, 236), (255, 190), (381, 200), (395, 352))
    level[1][3].append(poly)
    poly = ((-70, 300), (-76, 169), (-181, 174), (-290, 59), (-272, -202), (-162, -282), (47, -151), (162, -106), (285, -127), (400, -127), (400, -400), (-400, -400), (-400, 400), (-70, 400))
    level[1][3].append(poly)
    poly = ((39, 94), (-23, 59), (-41, -41), (51, -86), (147, -16), (109, 64))
    level[1][3].append(poly)

    poly = ((-184, 285), (-224, 230), (-250, 100), (-400, 100), (-400, 400), (-200, 400))
    level[1][2].append(poly)
    poly = ((-250, -100), (-200, -200), (-63, -247), (102, -287), (142,-146), (242, -101), (263, 23), (242, 174), (152, 199), (107, 282), (110, 400), (400, 400), (400, -400), (-400, -400), (-400, -100))
    level[1][2].append(poly)

    poly = ((-271, 310), (-320, 256), (-265, 183), (-187, 161), (-48, 185), (38, 256), (81, 320), (400, 400), (412, 245), (282, 183), (146, 115), (-27, 88), (-249, 137), (-456, 218), (-347, 430))
    level[2][1].append(poly)
    poly = ((-320, -70),  (-300, -90), (-227,-180), (-21, -237), (200, -200), (429, -91), (442, -509), (-532, -433))
    level[2][1].append(poly)

    poly = ((-100, 320), (-220, 200), (-300, 28), (-238, -10), (-200, -200), (-36, -160), (40, -242), (100, -225), (120, -162), (141, -183), (200, -37), (281, -37), (310, -117), (320, -320), (-320, -320), (-320, 320))
    level[2][0].append(poly)
    poly = ((140, 320), (180, 221), (280, 198), (320, 159), (320, 320))
    level[2][0].append(poly)

    poly = ((-250, 100), (-164, 221), (74, 306), (239, 240), (270, 100), (400, 100), (400, 400), (-400, 400), (-400, 100))
    level[2][3].append(poly)
    poly = ((270, -100), (188, -288), (-87, -259), (-196, -163), (-270, -100), (-400, -100), (-400, -400), (400, -400), (400, 100))
    level[2][3].append(poly)

    poly = ((400, 400), (400, 100), (250, 100), (132, 205), (63, 291), (-31, 296), (-95, 166), (-200, 200), (-320, 147), (-400, 147), (-400, 400))
    level[2][2].append(poly)
    poly = ((400, -100), (250, -100), (127, -235), (69, -129), (-11, -129), (-98, -219), (-281, -139), (-400, -139), (-400, -400), (400, -400))
    level[2][2].append(poly)
