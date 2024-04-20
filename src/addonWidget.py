#!/usr/bin/env python3
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic
import logging
from utils import *
import urllib

class AddonWidget(QtWidgets.QWidget):

    def __init__(self, steps=5, *args, **kwargs ):
        super(AddonWidget, self).__init__()

        self.client = ""

        # ======= UI ELEMENTS =========================
        self.parentLayout = QtWidgets.QHBoxLayout()
        self.textLayout = QtWidgets.QVBoxLayout()
        self.picLayout = QtWidgets.QVBoxLayout()
        self.installLayout = QtWidgets.QVBoxLayout()

        self.addon_image_label = QtWidgets.QLabel()
        self.addon_name_label = QtWidgets.QLabel("")
        self.addon_desc_label = QtWidgets.QLabel("Description :")
        self.addon_desc_label.setWordWrap(True)
        #self.addon_desc_text = QtWidgets.QLabel()
        self.install_button = QtWidgets.QPushButton("Install")
        self.install_button.clicked.connect(self.install_addon_button)
        self.picLayout.addWidget(self.addon_image_label)
        self.textLayout.addWidget(self.addon_name_label)
        self.textLayout.addWidget(self.addon_desc_label)
        self.installLayout.addWidget(self.install_button)
        #self.parentLayout.addWidget(self.addon_desc_text)

        self.parentLayout.addLayout(self.picLayout)
        self.parentLayout.addLayout(self.textLayout)
        self.parentLayout.addLayout(self.installLayout)

        self.setLayout(self.parentLayout)
        # ======= UI ELEMENTS =========================




    # Adds text to labels , url is the url of the photo  called after get_addon_desc() is called 
    def setup(self, name,client,desc,url):
        self.addon_name_label.setText(f"{name}")
        self.addon_desc_label.setText(desc)

        try: # try to set photo 
            url_photo = urllib.request.urlopen(url).read()
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(url_photo)
            self.addon_image_label.setPixmap(pixmap)
        except urllib.error.HTTPError as e:
            print("unable to find photo")

        self.client = client

        

    # Installs the addon to the client in profile.yml
    def install_addon_button(self):
       if self.client != "":
           self.client = self.client.lower()
           logger.debug(f'self.client: {self.client}')
           download_url = get_legacy_wow_addons(self.addon_name_label.text(), self.client) 
           install_addon(self.client, download_url)
           # TODO: unzip the installed zipfile 
           error = QtWidgets.QMessageBox.information(self, "Success", "Addon downloaded successfully")

       else:
           #TODO: add some popups for both when the download is done or coulden't start
           error = QtWidgets.QMessageBox.critical(self, "Error", "Client is not set ! ")

    def get_layout(self):
        return self.parentLayout 
