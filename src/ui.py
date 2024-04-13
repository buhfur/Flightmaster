#!/usr/bin/env python3

import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic
import logging
from utils import *
from addonWidget import AddonWidget


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

        print(self.addonsTabLayout.itemAt(0).widget() )

        


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



    # test function to see if I can add the elements from AddonWidget to the main window
    def test_add_to_window(self):
        self.addon_frame = QtWidgets.QVBoxLayout()
        self.addon_image_label = QtWidgets.QLabel()
        self.addon_name_label = QtWidgets.QLabel("Name:")
        self.addon_name_text = QtWidgets.QLabel("")
        self.addon_desc_label = QtWidgets.QLabel("Description :")
        self.addon_desc_text = QtWidgets.QLabel("")







app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
