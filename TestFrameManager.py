#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

In this example, we select a file with a
QFileDialog and display its contents
in a QTextEdit.

author: Jan Bodnar
website: zetcode.com
last edited: January 2015
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
    QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon

from SpreadsheetDOM import Workbooks
from SpreadsheetDOM.Collection import Collection

from TestFrame import Cluster

class TestFrameManagerMain(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QAction(QIcon('icons/page_white_excel.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open TestFrame cluster')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('TestFrame Manager')
        self.show()


    def showDialog(self):

        fname = QFileDialog.getOpenFileName(self, 'Open TestFrame cluster', './', "LibreOffice Calc (*.ods)")
        wb = Workbooks.OpenWorkbook(fname[0])

        for sheet in wb.Sheets:
            self.textEdit.append(sheet.Name)

        self.textEdit.append("------")
        cluster = Cluster(wb)
        print("Cluster %s. ID: %s" % (cluster.name, cluster.id))

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = TestFrameManagerMain()
    sys.exit(app.exec_())
