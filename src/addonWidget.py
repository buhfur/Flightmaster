#!/usr/bin/env python3
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QFrame
from PyQt6 import uic
import logging
from utils import *
import urllib

class AddonWidget(QtWidgets.QFrame):

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
        self.install_button = QtWidgets.QPushButton("Install")
        self.install_button.clicked.connect(self.install_addon_button)
        self.picLayout.addWidget(self.addon_image_label)
        self.textLayout.addWidget(self.addon_name_label)
        self.textLayout.addWidget(self.addon_desc_label)
        self.installLayout.addWidget(self.install_button)

        self.parentLayout.addLayout(self.picLayout)
        self.parentLayout.addLayout(self.textLayout)
        self.parentLayout.addLayout(self.installLayout)

        self.setLayout(self.parentLayout)
        # ======= UI ELEMENTS =========================
        self.setFrameStyle(QtWidgets.QFrame.Shape.Panel | QtWidgets.QFrame.Shadow.Plain)



    # Takes data from profile.yml and displays it  
    def setup(self, name,client,desc,url):
        self.addon_name_label.setText(f"{name}")
        self.addon_desc_label.setText(desc)
        pixmap = QtGui.QPixmap()
        try: # try to set photo 
            url_photo = urllib.request.urlopen(url).read()
            pixmap.loadFromData(url_photo)
            self.addon_image_label.setPixmap(pixmap)
        except urllib.error.HTTPError as e:
            pixmap = QtGui.QPixmap('./images/placeholder.png')
            logger.debug("unable to find photo")

        self.addon_image_label.setPixmap(pixmap) 
        self.client = client

        

    # Installs the addon to the client in profile.yml
    def install_addon_button(self):
       if self.client != "":
           self.client = self.client.lower()
           logger.debug(f'self.client: {self.client}')
           download_url = get_legacy_wow_addons(self.addon_name_label.text(), self.client) 
           if download_url == 0:
               error = QtWidgets.QMessageBox.critical(self, "Error", "Unable to find searched addon")
           else:
               # TODO: Find out why this is returning zero for an already installed addon
               zip_filename = install_addon(self.client, self.addon_name_label.text(),download_url)
               logger.debug(f'client: {self.client} \n addon label text {self.addon_name_label.text()}' )
               if zip_filename == 0 :
                   error = QtWidgets.QMessageBox.critical(self, "Error", "Addon is already installed")

               has_client = unzip_addon(zip_filename,self.client)
               if has_client == 0 :
                   client_error = QtWidgets.QMessageBox.critical(self, "Error", f"Could not install. No client listed for {self.client} ")
               else:

                   download_success = QtWidgets.QMessageBox.information(self, "Success", "Addon downloaded successfully")

       else:
           error = QtWidgets.QMessageBox.critical(self, "Error", "Client is not set ! ")

