import turtle, math
from os import listdir
import engine, game, rockets, menu

class Rectangle(engine.GameObject):
    rect_id = 0
    rect_done = {}

    def __init__(self, p1, p2, color_in="white", color_edge="black", static=True):
        "Create a rectangle object with opposite corners p1 and p2"
        print(Rectangle.rect_id)
        if (p1, p2) in Rectangle.rect_done:
            name = Rectangle.rect_done[(p1, p2)]
        else:
            shape = turtle.Shape("compound")
            poly = (p1, (p2[0], p1[1]), p2, (p1[0], p2[1]))
            shape.addcomponent(poly, color_in, color_edge)
            name = "rectangle" + str(Rectangle.rect_id)
            Rectangle.rect_id += 1
            turtle.register_shape(name, shape)
        Rectangle.rect_done[(p1, p2)] = name
        super().__init__(0, 0, 0, 0, name, color_in, static)

class Ground(engine.GameObject):
    def __init__(self, compounds=[]):
        self.poly = compounds
        ground = turtle.Shape('compound')
        for poly in compounds:
            poly = tuple((-y, x) for (x, y) in poly)
            ground.addcomponent(poly, 'black')
        turtle.register_shape('ground', ground)
        super().__init__(0, 0, 0, 0, 'ground', 'black', True) #True beacause static objects

    def init_ground(level="lvl1"):
        assert game.Game.ground == "", "Ground already initialized"
        print("Initializing the ground...")
        path = "Files/" + level + "/ground.txt"
        with open(path, 'r') as f:
            lines = f.readlines()
            assert len(lines) % 2 == 0, "Unconsistent file: " + path
            for i in range(len(lines) // 2):
                points = lines[2 * i].split()
                pos = lines[2 * i + 1].split()
                posi, posj = int(pos[0]), int(pos[1])
                poly = []
                assert len(points) % 2 == 0, "Unconsistent file: " + path
                for j in range(len(points) // 2):
                    px, py = int(points[2 * j]), int(points[2 * j + 1])
                    poly.append((px, py))
                game.Game.level[posi][posj].append(poly)
        game.Game.ground = Ground(game.Game.level[game.Game.posi][game.Game.posj])

    def init_platforms():
        assert game.Game.platforms == [], "Platforms already initialized"
        for i in range(game.Game.height):
            platforms_i = []
            for j in range(game.Game.length):
                platforms_i_j = []
                for poly in game.Game.level[i][j]:
                    for k in range(len(poly)):
                        x1, y1 = poly[k]
                        x2, y2 = poly[k - 1] #[-1] = last element
                        if y1 == y2 and abs(y1) < game.Game.LENGTH / 2:
                            """horizontal lines of the ceiling are not a problem
                            it is taken into account while checking if the landing
                            is possible (rocket.y + rocket.radius > platform.y)"""
                            platforms_i_j.append(((x1, y1), (x2, y2)))
                platforms_i.append(platforms_i_j)
            game.Game.platforms.append(platforms_i)

class Door(engine.GameObject):
    ldoor = []
    doorsopened = 0

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

def orthogonal_projection(p1, p2, p3):
    "orthogonal projection of p3 on the line (p1, p2)"
    """The problem is the same as finding the solution of :
        [x2 - x1   y1 - y2] [y]   [-c]
        [y1 - y2   x1 - x2] [x] = [-cp]
    where (x1 - x1)y + (y1 - y2)x + c = 0 is the equation of (p1, p2)
    and (y1 - y2)y + (x1 - x2)x  +cp = 0 is the equation of the orthogonal of (p1, p2) containing p3"""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    det = -(x1 - x2) ** 2 - (y1 - y2) ** 2
    c = -(x2 - x1) * y2 - (y1 - y2) * x2
    cp = -(y1 - y2) * y3 - (x1 - x2) * x3
    y = (- c * (x1 - x2) + cp * (y1 - y2)) / det #Cramer's formula
    x = (- cp * (x2 - x1) + c * (y1 - y2)) / det
    return x, y

def collide_round_poly(roundobj, poly):
    "Checks if a round object collides with a polygon"
    p3 = (roundobj.x, roundobj.y)
    for i in range(len(poly)):
        p1 = poly[i - 1]
        p2 = poly[i]
        x1, y1 = p1
        x2, y2 = p2
        x, y = orthogonal_projection(p1, p2, p3)
        if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2): #the point is on the segment
            if math.sqrt((x - roundobj.x) ** 2 + (y - roundobj.y) ** 2) < roundobj.radius: #the object is close enough
                return True
    return False

def collide_gnd(roundobj):
    "Checks if a round objects collides with the ground"
    res = False
    for poly in game.Game.ground.poly:
        res = res or collide_round_poly(roundobj, poly)
    return res

def register_shape_from_path(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        l1 = lines[0].split()
        name = l1[0]
        shape_radius_maybe = l1[-1] #it is the radius if the file is a skin
        shape = turtle.Shape("compound")
        for line_part in lines[1:]:
            line = line_part.split()
            color_in = line[1]
            color_edge = line[2]
            if line[0] == "poly":
                poly = []
                assert len(line[3:]) % 2 == 0, "Unconsistent file: " + path
                for i in range(1, len(line) // 2):
                    x, y = float(line[2 * i + 1]), float(line[2 * i + 2])
                    poly.append((x, y))
                if "no_compound" in l1: #in order to change the color of the shape
                    shape = tuple(poly)
                else:
                    shape.addcomponent(poly, color_in, color_edge)
            elif line[0] == "circle":
                x_center, y_center = float(line[3]), float(line[4])
                radius = float(line[5])
                circle = make_circle((x_center, y_center), radius)
                shape.addcomponent(circle, color_in, color_edge)
        turtle.register_shape(name, shape)
        return name, shape_radius_maybe

def makeshape():
    for file in listdir("Files/global_shapes"): #every file in the directory
        path = "Files/global_shapes/" + file
        register_shape_from_path(path)
    for file in listdir("Files/skins"):
        path = "Files/skins/" + file
        name, radius = register_shape_from_path(path)
        if "_powered" not in name:
            menu.Menu.skin_list.append(name)
            menu.Menu.skin_radius_list.append(int(radius))
