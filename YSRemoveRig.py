from PySide2 import QtWidgets, QtCore
import shiboken2
import maya.OpenMayaUI as omui
import maya.cmds as cmds

TITLE = "Remove Rig"

class Gui(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Gui, self).__init__(parent)

        #WindowSetting
        self.setWindowTitle(TITLE)
        self.setObjectName("YS%s_Gui"%(TITLE))
        self.setWindowFlags(QtCore.Qt.Window)

        #MainLayout
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        button = QtWidgets.QPushButton("Remove")
        button.setMinimumSize(300, 100)
        main_layout.addWidget(button, 0, 0)

        button.clicked.connect(self.call)
        

    def call(self):
        selected = cmds.ls(sl=True)
        for sel in selected:
            if not cmds.attributeQuery("Ctrl", node=sel, exists=True):
                continue
            proxy = cmds.listRelatives(sel, c=True)[0]
            cmds.delete(proxy)
            cmds.delete(sel)
            cmds.inViewMessage(amg="Success !!", pos='midCenter', fade=True)

def show_Gui():
    """ウィンドウを表示"""
    for widget in QtWidgets.QApplication.allWidgets():
        if widget.objectName() == "YS%s_Gui"%(TITLE):
            widget.close()

    maya_main_window = shiboken2.wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
    window = Gui(parent=maya_main_window)
    window.show()