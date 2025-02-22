from PySide2 import QtWidgets, QtCore, QtGui
import shiboken2
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import os
import json

def SaveShape():
    savefile = os.path.join(cmds.internalVar(userPrefDir=True), "YSRigControlShape.json")
    ws = {}
    selection = cmds.ls(sl=True)

    for sel in selection:
        cv = cmds.listRelatives(sel, s=True)[0]
        cv_pos = []
        cv_knot = []

        for i in range(cmds.getAttr("%s.controlPoints"%(cv), size=True)):
            cv_pos.append(cmds.getAttr("%s.controlPoints[%d]"%(cv, i))[0])
            cv_knot.append(i)
            
        
        
        ws["CVpoints_%s"%(sel)] = cv_pos
        ws["CVknot_%s"%(sel)] = cv_knot
        
    with open(savefile, "w") as f:
        json.dump(ws, f, indent=4)

class Gui(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Gui, self).__init__(parent)

        #WindowSetting
        self.setWindowTitle("SaveShape")
        self.setObjectName("SaveShape_Gui")
        self.setWindowFlags(QtCore.Qt.Window)

        #MainLayout
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        self.button = QtWidgets.QPushButton("Save")
        self.button.setStyleSheet("background-color: rgb(200, 200, 200); color: rgb(0, 0, 0);")
        self.button.clicked.connect(self.call)

        main_layout.addWidget(self.button, 0, 0, 1, 2)


    def call(self):
        SaveShape()

def get_maya_main_window():
    """Mayaのメインウィンドウを取得"""
    main_window_ptr = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

def show_Gui():
    """ウィンドウを表示"""
    for widget in QtWidgets.QApplication.allWidgets():
        if widget.objectName() == "SaveShape_Gui":
            widget.close()

    maya_main_window = get_maya_main_window()
    window = Gui(parent=maya_main_window)
    window.show()