import odf.opendocument
from odf.table import Table, TableRow, TableCell, TableColumn
from odf.text import P

from .Cell import Cell

# http://stackoverflow.com/a/4544699/1846474
class GrowingList(list):
    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend([None]*(index + 1 - len(self)))
        list.__setitem__(self, index, value)

class Sheet(object):
    """docstring for Sheet"""

    def __init__(self, parent, ods_sheet):
        self.ods_sheet = ods_sheet
        self.parent = parent

        self.Name = ods_sheet.getAttribute("name")
        self.clonespannedcolumns = False

        self._readSheet()

    def __str__(self):
        return "Sheet(%s)" % self.Name

    def dump(self):
        print(self.Name)
        for r in range(self.RowCount):
            for c in self._rows[r]:
                print(c.Text, end='')
            print('')

    def _readSheet(self):
        sheet = self.ods_sheet

        rows = sheet.getElementsByType(TableRow)
        cols = sheet.getElementsByType(TableColumn)
        arrRows = []

        self._rowcount = 0
        self._colcount = 0


        # for each row
        for row in rows[:-2]:
            row_comment = ""
            arrCells = GrowingList()
            cells = row.getElementsByType(TableCell)

            # for each cell
            count = 0
            for cell in cells[:-1]:
                # repeated value?
                repeat = cell.getAttribute("numbercolumnsrepeated")
                if(not repeat):
                    repeat = 1
                    spanned = int(cell.getAttribute('numbercolumnsspanned') or 0)
                    # clone spanned cells
                    if self.clonespannedcolumns is not None and spanned > 1:
                        repeat = spanned

                c = Cell(self, cell)

                for rr in range(int(repeat)):  # repeated?
                    arrCells[count] = c
                    count += 1

            # if row contained something
            rows_repeated = int(row.getAttribute("numberrowsrepeated") or 1)
            self._rowcount = self._rowcount + rows_repeated
            arrRows.append(arrCells)
            if count>self._colcount:
                self._colcount = count

            #else:
            #    print ("Empty or commented row (", row_comment, ")")

        print("sheet '%s' dimension (%d, %d)" % (self.Name, self._rowcount, self._colcount))
        self._rows = arrRows

    @property
    def RowCount(self):
        return len(self._rows)

    @property
    def ColumnCount(self):
        return self._colcount

    def Cells(self, row, column):
        row = self._rows[row-1]
        if len(row)<column:
            return Cell(self)
        else:
            return row[column-1]
