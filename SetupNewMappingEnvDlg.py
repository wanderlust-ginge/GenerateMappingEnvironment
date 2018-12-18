import sys
import os
import yaml
import json
import random
import copy
from os.path import join
from math import floor, inf
from shutil import copyfile, rmtree
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import GenerateMappingEnvironment
import Utils

class SetupNewMappingEnvDlg(QWidget):
    def __init__(self):
        super().__init__()
        self.path_to_app_root_dir = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Select location of the application you'd like to map.")
        self.setGeometry(500, 500, 600, 70)
        self.setMinimumSize(600, 70)
        self.docm_label = QLabel("Enter path to the App you wish to begin mapping:", self)
        self.docm_label.move(5, 5)
        self.textbox_path_to_app_root_dir = QLineEdit(self)
        self.textbox_path_to_app_root_dir.move(5, 30)
        self.textbox_path_to_app_root_dir.resize(500, 25)
        self.button_open_file_dlg = QPushButton('', self)
        self.button_open_file_dlg.resize(25, 25)
        self.button_open_file_dlg.move(510, 30)
        self.button_open_file_dlg.clicked.connect(self.on_click_open_file_dlg)
        open_folder_icon = QPixmap("icons/openedfolder.png")
        open_folder_icon = open_folder_icon.scaled(25, 25, Qt.KeepAspectRatio)
        self.button_open_file_dlg.setIcon(QIcon(open_folder_icon))
        self.button_confirm_set_env = QPushButton('Setup Mapping Environment', self)
        ok_icon = QPixmap("icons/ok.png")
        ok_icon = ok_icon.scaled(25, 25, Qt.KeepAspectRatio)
        self.button_confirm_set_env.setIcon(QIcon(ok_icon))
        self.button_confirm_set_env.resize(170, 25)
        self.button_confirm_set_env.move(5, 65)
        self.button_confirm_set_env.clicked.connect(self.on_click_confirm_set_env)
        self.button_cancel = QPushButton('Cancel', self)
        cancel_icon = QPixmap("icons/cancel.png")
        cancel_icon = cancel_icon.scaled(25, 25, Qt.KeepAspectRatio)
        self.button_cancel.setIcon(QIcon(cancel_icon))
        self.button_cancel.resize(60, 25)
        self.button_cancel.move(180, 65)
        self.button_cancel.clicked.connect(self.on_click_cancel)
        self.path_to_app = ""
        self.path_to_mappers = ""

    def on_click_open_file_dlg(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dir_path = QFileDialog.getExistingDirectory(self, "Select directory location", "C:/", options=options)
        if dir_path:
            self.path_to_app_root_dir = dir_path
            self.textbox_path_to_app_root_dir.setText(dir_path)

    def on_click_confirm_set_env(self):
        app_name = self.path_to_app_root_dir.split('/')[-1]
        path_to_mappers = join(self.path_to_app_root_dir, 'src', app_name + '.Mapper')
        path_to_app = join(self.path_to_app_root_dir, 'src', app_name, 'bin/Debug', app_name + '.exe')
        Utils.save_local_paths('', path_to_app, path_to_mappers)

        GenerateMappingEnvironment.GenerateMappingEnvironment(self.path_to_app_root_dir)
        self.close()

    def on_click_cancel(self):
        self.close()