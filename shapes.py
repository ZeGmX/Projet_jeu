import engine
import turtle


class Ground(engine.GameObject):
    def __init__(self, compounds=[]):
        self.poly = compounds
        ground = turtle.Shape('compound')
        for poly in compounds:
            poly = tuple((-y, x) for (x, y) in poly)
            ground.addcomponent(poly, 'black')
        turtle.register_shape('ground', ground)
        super().__init__(0, 0, 0, 0, 'ground', 'black')


class Door(engine.GameObject):
    def __init__(self, x, y, color, angle=0):
        self.angle = angle
        super().__init__(x, y, 0, 0, 'door', color)
        engine.del_obj(self)

    def heading(self):
        return self.angle


class Key(engine.GameObject):
    def __init__(self, x, y, color):
        super().__init__(x, y, 0, 0, 'key', color)
        engine.del_obj(self)



def make_circle(point, radius):
    turtle.seth(90)
    turtle.setpos(point[0] + radius, point[1])
    turtle.begin_poly()
    turtle.circle(radius)
    turtle.end_poly()
    return turtle.get_poly()
