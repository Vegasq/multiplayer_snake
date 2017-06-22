from objects.common import Cell, CellStack, Killable


class Apple(CellStack, Killable):
    def __init__(self, x, y):
        super(Apple, self).__init__()
        c = AppleCell(x, y)
        c.set_owner(self)
        self.add_cell(c)


class AppleCell(Cell):
    printable_symbol = "@"
