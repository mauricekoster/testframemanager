from .Workbook import Workbook
import os

def OpenWorkbook(filename):
    print(os.path.realpath(filename))
    return Workbook(os.path.realpath(filename))
