import xlwings as xl

from ..Collection import Collection
from .Sheet import Sheet

class Workbook(object):

    # loads the file
    def __init__(self, filename):
        self.wb = xl.Book(filename)
        self.Sheets = Collection()
        self.SHEET_NAMES = []
        for xlsheet in self.wb.sheets :
            sheetname = xlsheet.name
            self.SHEET_NAMES.append(sheetname)
            sheet = Sheet(self, xlsheet)
            print(sheetname, sheet.Name)
            self.Sheets.Add(sheet, sheet.Name)

    def has_sheet(self, name):
        return name in self.SHEET_NAMES