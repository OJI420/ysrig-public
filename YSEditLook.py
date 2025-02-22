from PySide2 import QtWidgets, QtCore
import shiboken2
import maya.OpenMayaUI as omui
import maya.cmds as cmds

TITLE = "Edit Look"

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

        col = ["0, 0, 0"] * 39
        i = 0
        col[i] = "255, 0, 0"
        i += 1
        col[i] = "255, 127, 0"
        i += 1
        col[i] = "255, 255, 0"
        i += 1
        col[i] = "127, 255, 0"
        i += 1
        col[i] = "0, 255, 0"
        i += 1
        col[i] = "0, 255, 127"
        i += 1
        col[i] = "0, 255, 255"
        i += 1
        col[i] = "0, 127, 255"
        i += 1
        col[i] = "0, 0, 255"
        i += 1
        col[i] = "127, 0, 255"
        i += 1
        col[i] = "255, 0, 255"
        i += 1
        col[i] = "255, 0, 127"
        i += 1
        col[i] = "127, 127, 127"
        i += 1
        col[i] = "255, 127, 127"
        i += 1
        col[i] = "255, 191, 127"
        i += 1
        col[i] = "255, 255, 127"
        i += 1
        col[i] = "191, 255, 127"
        i += 1
        col[i] = "127, 255, 127"
        i += 1
        col[i] = "127, 255, 191"
        i += 1
        col[i] = "127, 255, 255"
        i += 1
        col[i] = "127, 191, 255"
        i += 1
        col[i] = "127, 127, 255"
        i += 1
        col[i] = "191, 127, 255"
        i += 1
        col[i] = "255, 127, 255"
        i += 1
        col[i] = "255, 127, 191"
        i += 1
        col[i] = "255, 255, 255"
        i += 1
        col[i] = "127, 0, 0"
        i += 1
        col[i] = "127, 63, 0"
        i += 1
        col[i] = "127, 127, 0"
        i += 1
        col[i] = "63, 127, 0"
        i += 1
        col[i] = "0, 127, 0"
        i += 1
        col[i] = "0, 127, 63"
        i += 1
        col[i] = "0, 127, 127"
        i += 1
        col[i] = "0, 63, 127"
        i += 1
        col[i] = "0, 0, 127"
        i += 1
        col[i] = "63, 0, 127"
        i += 1
        col[i] = "127, 0, 127"
        i += 1
        col[i] = "127, 0, 63"
        i += 1
        col[i] = "0, 0, 0"

        j = 0
        k = 0
        for i in range(39):
            button = QtWidgets.QPushButton()
            button.setMinimumSize(40, 40)
            button.setMaximumSize(40, 40)
            button.setStyleSheet("background-color: rgb(%s);"%(col[i]))
            if i == 13 or i == 26:
                j += 1
                k += 13
            main_layout.addWidget(button, j, i - k)
            button.clicked.connect(self.setColor)

        label = QtWidgets.QLabel("Curve Width :")
        label.setAlignment(QtCore.Qt.AlignCenter)

        self.width_box = QtWidgets.QDoubleSpinBox()
        self.width_box.setRange(0.1, 100.0)
        self.width_box.setDecimals(2)
        self.width_box.setValue(1.0)
        self.width_box.setSingleStep(0.1)

        width_button = QtWidgets.QPushButton("Set Width")
        width_button.setStyleSheet("background-color: rgb(200, 200, 200); color: rgb(0, 0, 0);")
        
        main_layout.addWidget(label, 3, 0, 1, 4)
        main_layout.addWidget(self.width_box, 3, 4, 1, 5)
        main_layout.addWidget(width_button, 3, 9, 1, 4)

        self.width_box.valueChanged.connect(self.setWidth)
        width_button.clicked.connect(self.setWidth)

    def setColor(self):
        click_button = self.sender()
        col = click_button.palette().button().color()
        col = [col.red() / 255.0, col.green() / 255.0, col.blue() / 255.0]

        sel = cmds.ls(sl=True)
        for s in sel:
            tf = [s]
            if cmds.attributeQuery("Ctrl", node=s, exists=True):
                tf = cmds.listConnections("%s.Ctrl"%(s), s=True, d=False)
            for t in tf:
                shape = cmds.listRelatives(t, s=True)
                for sh in shape:
                    cmds.setAttr("%s.overrideEnabled"%(sh), 1)
                    cmds.setAttr("%s.overrideRGBColors"%(sh), 1)
                    cmds.setAttr("%s.overrideColorRGB"%(sh), col[0], col[1], col[2])
                    
    def setWidth(self):
        width = self.width_box.value()

        sel = cmds.ls(sl=True)
        for s in sel:
            tf = [s]
            if cmds.attributeQuery("Ctrl", node=s, exists=True):
                tf = cmds.listConnections("%s.Ctrl"%(s), s=True, d=False)
            for t in tf:
                shape = cmds.listRelatives(t, s=True)
                if not shape:
                    continue
                for sh in shape:
                    try:
                        cmds.setAttr("%s.lineWidth"%(sh), width)
                    except:
                        pass


def show_Gui():
    """ウィンドウを表示"""
    for widget in QtWidgets.QApplication.allWidgets():
        if widget.objectName() == "YS%s_Gui"%(TITLE):
            widget.close()

    maya_main_window = shiboken2.wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
    window = Gui(parent=maya_main_window)
    window.show()