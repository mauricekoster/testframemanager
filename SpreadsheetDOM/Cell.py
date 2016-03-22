from odf.text import P

class Cell(object):
    """docstring for Cell"""
    def __init__(self, parent, ods_cell=None):
        self.parent = parent
        self.ods_cell = ods_cell

    @property
    def Text(self):
        if not hasattr(self, '_text'):
            textContent = None
            if self.ods_cell:
                ps = self.ods_cell.getElementsByType(P)

                # for each text/text:span node
                if ps:
                    textContent = ""
                    for p in ps:
                        for n in p.childNodes:
                            if (n.nodeType == 1 and n.tagName == "text:span"):
                                for c in n.childNodes:
                                    if (c.nodeType == 3):
                                        textContent = u'{}{}'.format(textContent, n.data)

                            if (n.nodeType == 3):
                                textContent = u'{}{}'.format(textContent, n.data)
            self._text = textContent

        return self._text

    @property
    def Style(self):
        sn = self.ods_cell.getAttribute('stylename')
        sp = self.parent.parent.getParentStyle(sn)
        return sp

    def __str__(self):
        return self.Text
