from PySide2 import QtWidgets, QtCore
import shiboken2
import maya.OpenMayaUI as omui
import maya.cmds as cmds

TITLE = "Hide UtilityNode"

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

        button1 = QtWidgets.QPushButton("Show")
        button1.setMinimumSize(300, 50)
        main_layout.addWidget(button1, 0, 0)

        button1.clicked.connect(self.node_show)
        
        button2 = QtWidgets.QPushButton("Hide")
        button2.setMinimumSize(300, 50)
        main_layout.addWidget(button2, 1, 0)

        button2.clicked.connect(self.node_hide)

    def node_show(self):
        show = True
        self.main(show)

    def node_hide(self):
        show = False
        self.main(show)

    def main(self, show):
        nodes = cmds.ls()
        for node in nodes:
            if not cmds.attributeQuery("visibility", node=node, exists=True):
                cmds.setAttr("%s.ihi" %(node), show)

def show_Gui():
    """ウィンドウを表示"""
    for widget in QtWidgets.QApplication.allWidgets():
        if widget.objectName() == "YS%s_Gui"%(TITLE):
            widget.close()

    maya_main_window = shiboken2.wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
    window = Gui(parent=maya_main_window)
    window.show()