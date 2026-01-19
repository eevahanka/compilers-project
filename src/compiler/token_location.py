from dataclasses import dataclass

@dataclass
class Location:
    row: int
    column: int
    dummy: bool

    def __init__(self, row, column, dummy=False):
        self.row = row
        self.column = column
        self.dummy = dummy

    def __eq__(self, value):
        if self.row == value.row and self.column == value.column:
            return True
        elif self.dummy or value.dummy:
            return True
        return False
