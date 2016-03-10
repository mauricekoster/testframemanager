import odf.opendocument
from odf.table import Table

class Workbook:

    # loads the file
    def __init__(self, file, clonespannedcolumns=None):
        self.clonespannedcolumns = clonespannedcolumns
        self.doc = odf.opendocument.load(file)
        self.SHEETSNAMES = []
        self.SHEETS = {}
        for sheet in self.doc.spreadsheet.getElementsByType(Table):
            self.SHEETSNAMES.append(sheet.getAttribute('name'))
