from PySide2 import QtWidgets, QtCore, QtGui
import shiboken2
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import os
import json
import YSRig.YSRig as YSRig

class Json:
    def __init__(self):
        savefile = os.path.join(cmds.internalVar(userPrefDir=True), "YSRigControlShape.json")
        self.ld = {}
        if os.path.exists(savefile):
            with open(savefile, "r") as f:
                self.ld = json.load(f)
    def getKeys(self):
        keys = list(self.ld.keys())
        name = []
        for i, k in enumerate(keys):
            if i % 2:
                name.append(k.replace("CVknot_", ""))
        return name

class Gui(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Gui, self).__init__(parent)

        #WindowSetting
        self.setWindowTitle("YSCreateController")
        self.setObjectName("YSCreateController_gui")
        self.setWindowFlags(QtCore.Qt.Window)

        #MainLayout
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        j = Json()
        
        label = QtWidgets.QLabel("Shape :")
        self.dropdown = QtWidgets.QComboBox()
        self.dropdown.addItems(j.getKeys())
        main_layout.addWidget(label, 0, 0)
        main_layout.addWidget(self.dropdown, 0, 1, 1, 2)

        self.button = QtWidgets.QPushButton("Create")
        self.button.setStyleSheet("background-color: rgb(200, 200, 200); color: rgb(0, 0, 0);")
        self.button.clicked.connect(self.call)

        main_layout.addWidget(self.button, 1, 0, 1, 3)


    def call(self):
        shape = self.dropdown.currentText()
        YSRig.CreateCV(shape=shape, name=shape)

def get_maya_main_window():
    """Mayaのメインウィンドウを取得"""
    main_window_ptr = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

def show_Gui():
    """ウィンドウを表示"""
    for widget in QtWidgets.QApplication.allWidgets():
        if widget.objectName() == "YSCreateController_gui":
            widget.close()

    maya_main_window = get_maya_main_window()
    window = Gui(parent=maya_main_window)
    window.show()