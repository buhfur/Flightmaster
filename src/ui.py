#!/usr/bin/env python3

import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic
import logging
from utils import *


'''
Custom widget for presenting the addons 
'''
class AddonWidget(QtWidgets.QWidget):

    def __init__(self, steps=5, *args, **kwargs):
        super(AddonWidget, self).__init__(*args,**kwargs)
        self.layout = QtWidgets.QVBoxLayout()
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

        uic.loadUi("ui/main.ui", self)
        self.searchButton.clicked.connect(self.search_button)

        # Radio buttons on "Install Addons" tab
        self.searchVanillaButton.toggled.connect(self.search_radio_buttons)
        self.searchTbcButton.toggled.connect(self.search_radio_buttons)
        self.searchWotlkButton.toggled.connect(self.search_radio_buttons)
        self.searchCataButton.toggled.connect(self.search_radio_buttons)

        # Radio buttons on the "Add Clients" tab
        self.addClientVanilla.toggled.connect(self.add_client_radio_buttons)
        self.addClientTbc.toggled.connect(self.add_client_radio_buttons)
        self.addClientWotlk.toggled.connect(self.add_client_radio_buttons)
        self.addClientCata.toggled.connect(self.add_client_radio_buttons)
        self.addClientButton.clicked.connect(self.add_client_button)

        self.searchBar.setText("AtlasLoot")
        # Holds the values of the selected radio buttons on each tab 
        self.add_client_xpac = ""
        self.search_client_xpac = ""


        # Opens the file explorer
        if sys.platform.startswith("linux"):
            self.fileDialog = QtWidgets.QFileDialog

    # Search button to search for addons , uses AddonWidget to populate listview
    def search_button(self):
        addon_name = self.searchBar.text()
        addon_desc = get_addon_desc(addon_name,self.search_client_xpac)
        # Set text of addon labels 
        search_result_widget = AddonWidget().setup(addon_name,self.search_client_xpac,addon_desc[0], addon_desc[1])
        
        # searchView = self.searchAddonsTab.findChildren(QtWidgets.QListView)
        self.listAddonsWidget.addItem(search_result_widget)


    # Adds client Interface/Addons path for addon installations 
    def add_client_button(self):

        # pull what radio button was selected
        if sys.platform.startswith("linux"):
            print("linux detected")
            fs = self.fileDialog.getExistingDirectory(self, "/home/")

        elif sys.platform.startswith("win32"):
            print("windows detected")
            fs = self.fileDialog.getExistingDirectory(self, "C:\\Users\\", QFileDialog.DontUseNativeDialog )


        add_client_to_profile(self.add_client_xpac.lower(), fs)
        #All this does is pretty print the profile.yml
        utils.p_profile()


    # Handler for the "Install Addons" tab buttons 
    def search_radio_buttons(self):
        self.search_client_xpac = self.sender().text()

        
    # Handler for the "Add Clients" tab buttons 
    def add_client_radio_buttons(self):
        self.add_client_xpac = self.sender().text()





app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
