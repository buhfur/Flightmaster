
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6 import uic
import logging
from utils import *
from addonWidget import AddonWidget

class addonListModel(QtCore.QAbstractListModel):
    def __init__(self,parent=None):

        self.test = ""

    def rowCount(self):
        return 

    def columnCount(self):
        return 
    
    def data(self,index,role=Qt.ItemDataRole.DisplayRole):
        return None


# myAddonsLayout is the parent vertical layout
class addonList(QtWidgets.QWidget):

    def __init__(self, steps=5, *args, **kwargs ):
        super(addonList, self).__init__()
        
        # Testing out using listviews 

        self.addonListWidget = QtWidgets.QListWidget()

        self.addonListWidget.addItem(QtWidgets.QListWidgetItem("test", self.addonListWidget))



