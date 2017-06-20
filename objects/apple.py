from objects.common import Cell, CellStack


class Apple(CellStack):
    def __init__(self):
        super(Apple, self).__init__()
        c = Cell(3, 3)
        self.add_cell(c)
