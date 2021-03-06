import odf.opendocument
from odf.table import Table
from odf.style import Style

from .Collection import Collection
from .Sheet import Sheet

class Workbook(object):

    # loads the file
    def __init__(self, filename, clonespannedcolumns=None):
        self.clonespannedcolumns = clonespannedcolumns
        print("Loading file: %s" % filename)
        with open(filename, 'rb') as f:
            self.doc = odf.opendocument.load(f)

        self.SHEETSNAMES = []
        self.Sheets = Collection()
        for ods_sheet in self.doc.spreadsheet.getElementsByType(Table):
            sheet = Sheet(self, ods_sheet)
            self.Sheets.Add(sheet, sheet.Name)
            self.SHEETSNAMES.append(sheet.Name)

    def has_sheet(self, name):
        return name in self.SHEETSNAMES

    def getParentStyle(self, stylename):
        s = self.doc.getStyleByName(stylename)
        return s.getAttribute('parentstylename')