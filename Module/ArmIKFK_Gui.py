import json
import os
from PySide2 import QtWidgets, QtCore, QtGui
import shiboken2
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import importlib
import YSRig.Module.ArmIKFK as ArmIKFK
importlib.reload(ArmIKFK)

TITLE = "ArmIKFK"

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

        label1 = QtWidgets.QLabel("Group Name :")
        label1.setAlignment(QtCore.Qt.AlignRight)
        self.part_field = QtWidgets.QLineEdit()
        self.part_field.setPlaceholderText("Part")
        self.dropdown00 = QtWidgets.QComboBox()
        self.dropdown00.addItems(self.data.get("Arm"))
        main_layout.addWidget(label1, i, 0)
        main_layout.addWidget(self.part_field, i, 1)
        main_layout.addWidget(self.dropdown00, i, 2)

        self.part_field.setText(self.dropdown00.currentText())
        self.dropdown00.currentIndexChanged.connect(self.setPreset)

        i += 1

        label2 = QtWidgets.QLabel("Search & Replace :")
        label2.setAlignment(QtCore.Qt.AlignRight)
        self.s_field = QtWidgets.QLineEdit()
        self.r_field = QtWidgets.QLineEdit()
        self.s_field.setPlaceholderText("Search")
        self.s_field.setText(self.data.get("Search"))
        self.r_field.setPlaceholderText("Replace")
        self.r_field.setText(self.data.get("Replace"))
        main_layout.addWidget(label2, i, 0)
        main_layout.addWidget(self.s_field, i, 1)
        main_layout.addWidget(self.r_field, i, 2)

        i += 1

        frame1 = QtWidgets.QFrame()
        frame1.setFrameShape(QtWidgets.QFrame.HLine)
        frame1.setFrameShadow(QtWidgets.QFrame.Sunken)

        main_layout.addWidget(frame1, i, 0, 1, 3)

        i += 1

        label3 = QtWidgets.QLabel("FK Controller Shape :")
        label3.setAlignment(QtCore.Qt.AlignRight)
        self.dropdown01 = QtWidgets.QComboBox()
        self.dropdown01.addItems(["cube", "circle", "square"])
        main_layout.addWidget(label3, i, 0)
        main_layout.addWidget(self.dropdown01, i, 1, 1, 2)

        i += 1

        label4 = QtWidgets.QLabel("FK Controller Scale :")
        label4.setAlignment(QtCore.Qt.AlignRight)
        self.fk_scale_field = QtWidgets.QDoubleSpinBox()
        self.fk_scale_field.setRange(0.1, 100.0)
        self.fk_scale_field.setDecimals(2)
        self.fk_scale_field.setValue(1.0)
        self.fk_scale_field.setSingleStep(0.1)
        main_layout.addWidget(label4, i, 0)
        main_layout.addWidget(self.fk_scale_field, i, 1, 1, 2)

        i += 1

        label5 = QtWidgets.QLabel("IK Handle Controller Shape :")
        label5.setAlignment(QtCore.Qt.AlignRight)
        self.dropdown02 = QtWidgets.QComboBox()
        self.dropdown02.addItems(["locator", "sphere", "octahedron"])
        main_layout.addWidget(label5, i, 0)
        main_layout.addWidget(self.dropdown02, i, 1, 1, 2)

        i += 1

        label6 = QtWidgets.QLabel("PoleVector Controller Shape :")
        label6.setAlignment(QtCore.Qt.AlignRight)
        self.dropdown03 = QtWidgets.QComboBox()
        self.dropdown03.addItems(["locator", "sphere", "octahedron"])
        main_layout.addWidget(label6, i, 0)
        main_layout.addWidget(self.dropdown03, i, 1, 1, 2)

        i += 1

        label7 = QtWidgets.QLabel("Elbow Vector :")
        label7.setAlignment(QtCore.Qt.AlignRight)
        self.dropdown04 = QtWidgets.QComboBox()
        self.dropdown04.addItems(["Y+", "Y-", "Z+", "Z-"])
        main_layout.addWidget(label7, i, 0)
        main_layout.addWidget(self.dropdown04, i, 1, 1, 2)

        i += 1

        label8 = QtWidgets.QLabel("IK Controller Scale :")
        label8.setAlignment(QtCore.Qt.AlignRight)
        self.ik_scale_field = QtWidgets.QDoubleSpinBox()
        self.ik_scale_field.setRange(0.1, 100.0)
        self.ik_scale_field.setDecimals(2)
        self.ik_scale_field.setValue(1.0)
        self.ik_scale_field.setSingleStep(0.1)
        main_layout.addWidget(label8, i, 0)
        main_layout.addWidget(self.ik_scale_field, i, 1, 1, 2)

        i += 1

        label9 = QtWidgets.QLabel("PoleVector Length :")
        label9.setAlignment(QtCore.Qt.AlignRight)
        self.ik_length_field = QtWidgets.QDoubleSpinBox()
        self.ik_length_field.setRange(0.1, 100.0)
        self.ik_length_field.setDecimals(2)
        self.ik_length_field.setValue(1.0)
        self.ik_length_field.setSingleStep(0.1)
        main_layout.addWidget(label9, i, 0)
        main_layout.addWidget(self.ik_length_field, i, 1, 1, 2)

        i += 1

        label10 = QtWidgets.QLabel("Hand Controller Shape :")
        label10.setAlignment(QtCore.Qt.AlignRight)
        self.dropdown05 = QtWidgets.QComboBox()
        self.dropdown05.addItems(["circle", "cube", "square", "hand"])
        main_layout.addWidget(label10, i, 0)
        main_layout.addWidget(self.dropdown05, i, 1, 1, 2)

        i += 1

        label11 = QtWidgets.QLabel("Hand Controller Scale :")
        label11.setAlignment(QtCore.Qt.AlignRight)
        self.hand_scale_field = QtWidgets.QDoubleSpinBox()
        self.hand_scale_field.setRange(0.1, 100.0)
        self.hand_scale_field.setDecimals(2)
        self.hand_scale_field.setValue(1.0)
        self.hand_scale_field.setSingleStep(0.1)
        main_layout.addWidget(label11, i, 0)
        main_layout.addWidget(self.hand_scale_field, i, 1, 1, 2)

        i += 1

        frame1 = QtWidgets.QFrame()
        frame1.setFrameShape(QtWidgets.QFrame.HLine)
        frame1.setFrameShadow(QtWidgets.QFrame.Sunken)

        main_layout.addWidget(frame1, i, 0, 1, 3)

        i += 1

        self.button = QtWidgets.QPushButton("Apply")
        self.button.setStyleSheet("background-color: rgb(200, 200, 200); color: rgb(0, 0, 0);")
        self.button.clicked.connect(self.call)

        main_layout.addWidget(self.button, i, 0, 1, 3)


    def call(self):
        jt_list = cmds.ls(sl=True)
        part = self.part_field.text()
        search = self.s_field.text()
        replace = self.r_field.text()
        fk_shape = self.dropdown01.currentText()
        fk_scale = self.fk_scale_field.value()
        hd_shape = self.dropdown02.currentText()
        pv_shape = self.dropdown03.currentText()
        axis = self.dropdown04.currentText()
        ik_scale = self.ik_scale_field.value()
        ik_length = self.ik_length_field.value()
        hand_shape = self.dropdown05.currentText()
        hand_scale = self.hand_scale_field.value()
        if not part or not search or not replace:
            cmds.error("Input information is missing.")
        ArmIKFK.main(part, jt_list, [search, replace], scale=fk_scale, handScale=hand_scale, shape=fk_shape, handShape=hand_shape, pvAxis=axis, hds=hd_shape, pvs=pv_shape, length=ik_length, ik_scale=ik_scale)

    def setPreset(self):
        self.part_field.setText(self.dropdown00.currentText())

def get_maya_main_window():
    """Mayaのメインウィンドウを取得"""
    main_window_ptr = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

def show_Gui():
    """ウィンドウを表示"""
    for widget in QtWidgets.QApplication.allWidgets():
        if widget.objectName() == "YSArmIKFK_Gui":
            widget.close()

    maya_main_window = get_maya_main_window()
    window = Gui(parent=maya_main_window)
    window.show()