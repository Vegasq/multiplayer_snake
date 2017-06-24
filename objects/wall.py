import random
from objects.common import Cell, CellStack, Killable

wall_a = (
    (0, 0),
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (0, 5),
    (0, 6),
    (0, 7),
    (0, 8),
    (0, 9),
)

wall_b = (
    (0, 0),
    (1, 0),
    (2, 0),
    (3, 0),
    (4, 0),
    (5, 0),
    (6, 0),
    (7, 0),
    (8, 0),
    (9, 0),
)

wall_c = (
    (0, 0),
    (1, 0),
    (2, 0),
    (3, 0),
    (3, 1),
    (3, 2),
    (3, 3),
    (3, 4),
)


all_walls = (
    wall_a,
    wall_b,
    wall_c
)


class WallCell(Cell):
    printable_symbol = "*"


class Wall(CellStack, Killable):
    """
    It's Killable for cases when tail of wall out of screen.
    """
    def __init__(self, x, y):
        super(Wall, self).__init__()
        wall_template = random.choice(all_walls)

        for pos in wall_template:
            c = WallCell(x + pos[0], y + pos[1], hardness=10)
            c.set_owner(self)
            self.add_cell(c)
