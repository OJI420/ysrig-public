import json
import os
from PySide2 import QtWidgets, QtCore
import shiboken2
import maya.OpenMayaUI as omui
import maya.cmds as cmds

TITLE = "YSRig Settings"

class Gui(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Gui, self).__init__(parent)

        self.file = os.path.join(cmds.internalVar(userPrefDir=True), "YSRigSettings.json")
        self.data = {}
        with open(self.file, "r") as f:
            self.data = json.load(f)

        #WindowSetting
        self.setWindowTitle(TITLE)
        self.setObjectName("YS%s_Gui"%(TITLE))
        self.setWindowFlags(QtCore.Qt.Window)

        #MainLayout
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        i = 0

        label0 = QtWidgets.QLabel("Search & Replace :")
        label0.setAlignment(QtCore.Qt.AlignRight)
        self.line0 = QtWidgets.QLineEdit()
        self.line1 = QtWidgets.QLineEdit()
        self.line0.setPlaceholderText("Search")
        self.line0.setText(self.data.get("Search"))
        self.line1.setPlaceholderText("Replace")
        self.line1.setText(self.data.get("Replace"))
        main_layout.addWidget(label0, i, 0)
        main_layout.addWidget(self.line0, i, 1)
        main_layout.addWidget(self.line1, i, 2)

        i += 1

        label1 = QtWidgets.QLabel("SimpleFK Group Name Preset :")
        label1.setAlignment(QtCore.Qt.AlignRight)
        self.line2 = QtWidgets.QLineEdit()
        self.line2.setText(" ".join(self.data.get("FK")))
        main_layout.addWidget(label1, i, 0)
        main_layout.addWidget(self.line2, i, 1, 1, 2)
        
        i += 1

        label2 = QtWidgets.QLabel("Spine Group Name Preset :")
        label2.setAlignment(QtCore.Qt.AlignRight)
        self.line3 = QtWidgets.QLineEdit()
        self.line3.setText(" ".join(self.data.get("Spine")))
        main_layout.addWidget(label2, i, 0)
        main_layout.addWidget(self.line3, i, 1, 1, 2)
        
        i += 1

        label3 = QtWidgets.QLabel("NeckFK Group Name Preset :")
        label3.setAlignment(QtCore.Qt.AlignRight)
        self.line4 = QtWidgets.QLineEdit()
        self.line4.setText(" ".join(self.data.get("Neck")))
        main_layout.addWidget(label3, i, 0)
        main_layout.addWidget(self.line4, i, 1, 1, 2)
        
        i += 1

        label4 = QtWidgets.QLabel("ArmIKFK Group Name Preset :")
        label4.setAlignment(QtCore.Qt.AlignRight)
        self.line5 = QtWidgets.QLineEdit()
        self.line5.setText(" ".join(self.data.get("Arm")))
        main_layout.addWidget(label4, i, 0)
        main_layout.addWidget(self.line5, i, 1, 1, 2)

        i += 1

        label5 = QtWidgets.QLabel("LegIKFK Group Name Preset :")
        label5.setAlignment(QtCore.Qt.AlignRight)
        self.line6 = QtWidgets.QLineEdit()
        self.line6.setText(" ".join(self.data.get("Leg")))
        main_layout.addWidget(label5, i, 0)
        main_layout.addWidget(self.line6, i, 1, 1, 2)

        i += 1

        label6 = QtWidgets.QLabel("Finger Group Name Preset :")
        label6.setAlignment(QtCore.Qt.AlignRight)
        self.line7 = QtWidgets.QLineEdit()
        self.line7.setText(" ".join(self.data.get("Finger")))
        main_layout.addWidget(label6, i, 0)
        main_layout.addWidget(self.line7, i, 1, 1, 2)

        i += 1

        frame1 = QtWidgets.QFrame()
        frame1.setFrameShape(QtWidgets.QFrame.HLine)
        frame1.setFrameShadow(QtWidgets.QFrame.Sunken)

        main_layout.addWidget(frame1, i, 0, 1, 3)

        i += 1

        self.button = QtWidgets.QPushButton("Save")
        self.button.setStyleSheet("background-color: rgb(200, 200, 200); color: rgb(0, 0, 0);")
        self.button.clicked.connect(self.save)

        main_layout.addWidget(self.button, i, 0, 1, 3)

    def save(self):
        self.data["Search"] = self.line0.text()
        self.data["Replace"] = self.line1.text()
        self.data["FK"] = self.line2.text().split()
        self.data["Spine"] = self.line3.text().split()
        self.data["Neck"] = self.line4.text().split()
        self.data["Arm"] = self.line5.text().split()
        self.data["Leg"] = self.line6.text().split()
        self.data["Finger"] = self.line7.text().split()

        with open(self.file, "w") as f:
            json.dump(self.data, f, indent=4)



def show_Gui():
    """ウィンドウを表示"""
    for widget in QtWidgets.QApplication.allWidgets():
        if widget.objectName() == "YS%s_Gui"%(TITLE):
            widget.close()

    maya_main_window = shiboken2.wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
    window = Gui(parent=maya_main_window)
    window.show()