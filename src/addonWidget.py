#!/usr/bin/env python3
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic
import logging
from utils import *
import urllib

class AddonWidget(QtWidgets.QWidget):

    def __init__(self, steps=5,layout=None, *args, **kwargs ):
        super(AddonWidget, self).__init__()
        
        self.AddonWidgetLayout = QtWidgets.QVBoxLayout()

        #self.addon_desc_scroll = QtWidgets.QScrollArea()
        
        self.addon_image_label = QtWidgets.QLabel()
        self.addon_name_label = QtWidgets.QLabel("Name:")
        self.addon_desc_label = QtWidgets.QLabel("Description :")
        self.addon_desc_text = QtWidgets.QTextBrowser()
        



        self.client = ""
        self.install_button = QtWidgets.QPushButton("Install")
        self.install_button.clicked.connect(self.install_addon_button)
        
        
        self.AddonWidgetLayout.addWidget(self.addon_image_label)
        self.AddonWidgetLayout.addWidget(self.addon_name_label)
        self.AddonWidgetLayout.addWidget(self.addon_desc_label)
        self.AddonWidgetLayout.addWidget(self.addon_desc_text)
        self.AddonWidgetLayout.addWidget(self.install_button)

        #self.addon_desc_scroll.setWidget(self.addon_desc_text)
        #self.AddonWidgetLayout.addWidget(self.addon_desc_scroll)

        
        # Need to add the layout to the widget before it is added to the scrollview

        self.setLayout(self.AddonWidgetLayout)
        




    # Adds text to labels , url is the url of the photo  called after get_addon_desc() is called 
    def setup(self, name,client,desc,url):
        self.addon_name_label.setText(f"Name : {name}")
        self.addon_desc_text.setPlainText(desc)

        try: # try to set photo 
            url_photo = urllib.request.urlopen(url).read()
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(url_photo)
            self.addon_image_label.setPixmap(pixmap)
        except Exception as e:
            logger.debug("unable to find photo")

        self.client = client

        

    # Installs the addon to the client in profile.yml
    def install_addon_button(self):
       download_url = get_legacy_wow_addons(self.addon_name_text, self.client) 
       if self.client != "":
           install_addon(self.client, download_url)
       else:
           #TODO: add some popups for both when the download is done or coulden't start
           logger.debug("Client is not set ! ")

    def get_layout(self):
        return self.AddonWidgetLayout 
