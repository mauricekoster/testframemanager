from .Workbook import Workbook
import os


def OpenWorkbook(filename):
    try:
        return Workbook(os.path.realpath(filename))
    except Exception as e:
        raise IOError("Error reading LibreOffice file")
