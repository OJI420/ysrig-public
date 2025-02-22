import json
import os
from PySide2 import QtWidgets, QtCore, QtGui
import shiboken2
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import importlib
import YSRig.Module.Spine as Spine
importlib.reload(Spine)

TITLE = "Spine"

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
        
        label1 = QtWidgets.QLabel("Group Name :")
        label1.setAlignment(QtCore.Qt.AlignRight)
        self.part_field = QtWidgets.QLineEdit()
        self.part_field.setPlaceholderText("Part")
        self.dropdown00 = QtWidgets.QComboBox()
        self.dropdown00.addItems(self.data.get("Spine"))
        main_layout.addWidget(label1, 0, 0)
        main_layout.addWidget(self.part_field, 0, 1)
        main_layout.addWidget(self.dropdown00, 0, 2)

        self.part_field.setText(self.dropdown00.currentText())
        self.dropdown00.currentIndexChanged.connect(self.setPreset)


        label2 = QtWidgets.QLabel("Search & Replace :")
        label2.setAlignment(QtCore.Qt.AlignRight)
        self.s_field = QtWidgets.QLineEdit()
        self.r_field = QtWidgets.QLineEdit()
        self.s_field.setPlaceholderText("Search")
        self.s_field.setText(self.data.get("Search"))
        self.r_field.setPlaceholderText("Replace")
        self.r_field.setText(self.data.get("Replace"))
        main_layout.addWidget(label2, 1, 0)
        main_layout.addWidget(self.s_field, 1, 1)
        main_layout.addWidget(self.r_field, 1, 2)

        frame1 = QtWidgets.QFrame()
        frame1.setFrameShape(QtWidgets.QFrame.HLine)
        frame1.setFrameShadow(QtWidgets.QFrame.Sunken)

        main_layout.addWidget(frame1, 2, 0, 1, 3)

        label4 = QtWidgets.QLabel("Controller Scale :")
        label4.setAlignment(QtCore.Qt.AlignRight)
        self.scale_field = QtWidgets.QDoubleSpinBox()
        self.scale_field.setRange(0.1, 100.0)
        self.scale_field.setDecimals(2)
        self.scale_field.setValue(1.0)
        self.scale_field.setSingleStep(0.1)
        main_layout.addWidget(label4, 3, 0)
        main_layout.addWidget(self.scale_field, 3, 1, 1, 2)

        frame1 = QtWidgets.QFrame()
        frame1.setFrameShape(QtWidgets.QFrame.HLine)
        frame1.setFrameShadow(QtWidgets.QFrame.Sunken)

        main_layout.addWidget(frame1, 4, 0, 1, 3)

        label5 = QtWidgets.QLabel("Connect Type :")
        label5.setAlignment(QtCore.Qt.AlignRight)
        self.radioGroup = QtWidgets.QButtonGroup()

        self.radio1 = QtWidgets.QRadioButton("World")
        self.radio2 = QtWidgets.QRadioButton("Local")

        self.radioGroup.addButton(self.radio1, 1)
        self.radioGroup.addButton(self.radio2, 2)
        self.radio2.setChecked(True)

        main_layout.addWidget(label5, 5, 0)
        main_layout.addWidget(self.radio1, 5, 1)
        main_layout.addWidget(self.radio2, 5, 2)

        self.button = QtWidgets.QPushButton("Apply")
        self.button.setStyleSheet("background-color: rgb(200, 200, 200); color: rgb(0, 0, 0);")
        self.button.clicked.connect(self.call)

        main_layout.addWidget(self.button, 6, 0, 1, 3)


    def call(self):
        jt_list = cmds.ls(sl=True)
        part = self.part_field.text()
        search = self.s_field.text()
        replace = self.r_field.text()
        scale = self.scale_field.value()
        type = "World"
        if  self.radioGroup.checkedId() == 2: #返ってきたラジオボタンのIDが1なら　False
            type = "Local"
        if not part or not search or not replace:
            cmds.error("Input information is missing.")
        Spine.main(part, jt_list, [search, replace], scale=scale, cnnect=type)

    def setPreset(self):
        self.part_field.setText(self.dropdown00.currentText())
        
def get_maya_main_window():
    """Mayaのメインウィンドウを取得"""
    main_window_ptr = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

def show_Gui():
    """ウィンドウを表示"""
    for widget in QtWidgets.QApplication.allWidgets():
        if widget.objectName() == "YSSpine_Gui":
            widget.close()

    maya_main_window = get_maya_main_window()
    window = Gui(parent=maya_main_window)
    window.show()