from .Cell import Cell

class Sheet(object):
    def __init__(self, workbook, sheet):
        self.Workbook = workbook

        self.sheet = sheet

    @property
    def Name(self):
        
        return self.sheet.name

    @property
    def RowCount(self):
        #return self.sheet.cells.last_cell.row
        return self.sheet.api.UsedRange.Rows.Count

    @property
    def ColumnCount(self):
        return self.sheet.api.UsedRange.Columns.Count


    def Cells(self, row, column):
        cell = Cell(self, row, column)
        return cell