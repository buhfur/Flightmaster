#!/usr/bin/env python3

import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/ui-log.txt',filemode='w',encoding='utf-8', level=logging.DEBUG)




class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/main.ui", self)
        #self.button = self.searchButton
        self.searchButton.clicked.connect(self.search_button)
        if sys.platform.startswith("linux"):
            #self.fileDialog = QtWidgets.QFileDialog.getOpenFileName(self, "/home/")
            self.fileDialog = QtWidgets.QFileDialog
    # Search button to search for addons 
    def search_button(self):
        # Get text content of searchBar
        fs = self.fileDialog.getOpenFileName(self, "/home/")

        print((self.searchBar.text()))

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
