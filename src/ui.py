#!/usr/bin/env python3


import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6 import uic
import logging
from utils import *
from addonWidget import AddonWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        uic.loadUi("ui/main.ui", self)

        #=========== UI elements =========== 
        self.searchButton.clicked.connect(self.search_button)

        self.searchVanillaButton.toggled.connect(self.search_radio_buttons)
        self.searchTbcButton.toggled.connect(self.search_radio_buttons)
        self.searchWotlkButton.toggled.connect(self.search_radio_buttons)
        self.searchCataButton.toggled.connect(self.search_radio_buttons)

        self.addClientVanilla.toggled.connect(self.add_client_radio_buttons)
        self.addClientTbc.toggled.connect(self.add_client_radio_buttons)
        self.addClientWotlk.toggled.connect(self.add_client_radio_buttons)
        self.addClientCata.toggled.connect(self.add_client_radio_buttons)
        self.addClientButton.clicked.connect(self.add_client_button)

        #================ Testing temp widget  ===========
        self.container = QtWidgets.QWidget()
        self.containerLayout = QtWidgets.QVBoxLayout(self.container)

        #self.containerLayout.setContentsMargins(50,0,0,0)
        #self.containerLayout.setSpacing(50)

       
        #================ Scrollbar testing ===========
        self.scrollBar = QtWidgets.QScrollArea()
        self.scrollBar.setWidget(self.container)
        self.scrollBar.setWidgetResizable(True)
        self.scrollBar.resize(self.searchAddonsTab.sizeHint()) 
        self.searchAddonsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.xpacLayout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.searchAddonsLayout.addWidget(self.scrollBar) 


        #=========== UI elements end =========== 
        self.searchBar.setText("pfQuest")
        self.add_client_xpac = ""
        self.search_client_xpac = ""


        # Opens the file explorer
        if sys.platform.startswith("linux"):
            self.fileDialog = QtWidgets.QFileDialog

    # Search button to search for addons , uses AddonWidget to populate listview
    def search_button(self):
        addon_name = self.searchBar.text()
        addon_desc = get_addon_desc(addon_name,self.search_client_xpac)

        resultWidget = AddonWidget()
        resultWidget.setup(addon_name,self.search_client_xpac, addon_desc[0], addon_desc[1] )

        

        resultWidgetLayout = resultWidget.get_layout()

        
        #================ Testing temp widget  ===========
        self.containerLayout.addWidget(resultWidget)
        #================ Testing temp widget  ===========

        self.searchAddonsLayout.addWidget(self.scrollBar)# This fixed it for me  

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
