#!/usr/bin/env python3
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic
import logging
from utils import *

class AddonWidget(QtWidgets.QWidget):

    def __init__(self, layout, steps=5 ):
        super(AddonWidget, self).__init__()
        self.layout = layout
        self.addon_image_label = QtWidgets.QLabel()
        self.addon_name_label = QtWidgets.QLabel("Name:")
        self.addon_name_text = QtWidgets.QLabel("")
        self.addon_desc_label = QtWidgets.QLabel("Description :")
        self.addon_desc_text = QtWidgets.QLabel("")


        self.client = ""
        self.install_button = QtWidgets.QPushButton("Install")
        self.layout.addWidget(self.addon_image_label)
        self.layout.addWidget(self.addon_name_label)
        self.layout.addWidget(self.addon_name_text)
        self.layout.addWidget(self.addon_desc_label)
        self.layout.addWidget(self.addon_desc_text)
        self.layout.addWidget(self.install_button)

        self.install_button.clicked.connect(self.install_addon_button)
        self.setLayout(self.layout)

    # Adds text to labels , url is the url of the photo  called after get_addon_desc() is called 
    def setup(self, name,client,desc,url):
        self.addon_name_text.setText(name)
        self.addon_desc_text.setText(desc)
        self.addon_image_label.setPixmap(QtGui.QPixmap(url))
        self.client = client

        

    # Installs the addon to the client in profile.yml
    def install_addon_button(self):
       download_url = get_legacy_wow_addons(self.addon_name_text, self.client) 
       if self.client != "":
           install_addon(self.client, download_url)
       else:
           #TODO: add some popups for both when the download is done or coulden't start
           logger.debug("Client is not set ! ")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QGridLayout(self)
        self.addon_widget = AddonWidget(self.layout)




if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
