from objects.common import Cell
import settings


class Empty(Cell):
    printable_symbol = " "

    # def serialize_cell(self):
    #     return {
    #         "type": "EmptyCell",
    #         "color": settings.colors["background"],
    #         "printable_symbol": " "
    #     }
