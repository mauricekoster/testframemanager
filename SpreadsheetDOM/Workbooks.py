import os
import sys
import importlib

def load_module(modulename, package=None):
    mod = None
    try:
        mod = importlib.import_module(modulename, package)
    except ImportError:
        print("Failed to load {module}".format(module=modulename),
                    file=sys.stderr)
    return mod

def OpenWorkbook(filename):
    fn = os.path.realpath(filename)
    _, file_extension = os.path.splitext(fn)

    if file_extension in ['.xlsx']:
        module = load_module('.Excel', 'SpreadsheetDOM')

    klass = getattr(module, 'Workbook')
    try: 
        return klass(fn)

    except Exception as e:
        raise IOError("Error reading spreadsheet file")
