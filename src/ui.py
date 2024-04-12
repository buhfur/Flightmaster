#!/usr/bin/env python3

import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic
import logging
from utils import *





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

        # Holds the values of the selected radio buttons on each tab 
        self.add_client_xpac = ""
        self.search_client_xpac = ""

        # Opens the file explorer
        if sys.platform.startswith("linux"):
            self.fileDialog = QtWidgets.QFileDialog

    # Search button to search for addons 
    def search_button(self):
        return 0

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
        # Gotta make sure the file path is a string 

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
