import xlwings as xl

class Cell(object):
    def __init__(self, parent, row, column):
        self.sheet = parent
        self.row = row
        self.column = column
        self.cell = parent.sheet[row-1, column-1]

    @property
    def Text(self):
        if self.cell.value is None:
            return None
            
        return str(self.cell.value)

    @property
    def Style(self):
        return self.cell.api.Style.Name
