import random
from objects.common import Cell, CellStack, Killable
import settings

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

    def serialize_cell(self):
        return {
            "type": "SnakeCell",
            "color": self.get_owner().color,
            "printable_symbol": "*",
            "alive": self.get_owner().alive
        }


class Wall(CellStack, Killable):
    """
    It's Killable for cases when tail of wall out of screen.
    """

    def _create_frame(self):
        wall_template = []
        # top border
        for i in range(0, settings.columns):
            wall_template.append((i, 0))

        # bottom border
        for i in range(0, settings.columns):
            wall_template.append((i, settings.rows-1))

        # left border
        for i in range(1, settings.rows - 1):
            wall_template.append((0, i))

        # right border
        for i in range(1, settings.rows - 1):
            wall_template.append((settings.columns - 1, i))
        return wall_template

    def __init__(self, x, y, frame=False):
        super(Wall, self).__init__()
        self.is_frame = frame
        if self.is_frame:
            wall_template = self._create_frame()
            hard = 10
        else:
            wall_template = random.choice(all_walls)
            hard = 9

        for pos in wall_template:
            c = WallCell(x + pos[0], y + pos[1], hardness=hard)
            c.set_owner(self)
            self.add_cell(c)

        self.color = settings.colors["wall"]

    def kill(self):
        print("Killing wall frame=%s alive=%s" % (
            self.is_frame,
            self.alive
        ))
        super(Wall, self).kill()
