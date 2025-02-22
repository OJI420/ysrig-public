from importlib import *
import maya.cmds as cmds
import maya.mel as mel
import YSRig.YSCreateController as YSCreateController
import YSRig.Module.SimpleFK_Gui as SimpleFK_Gui
import YSRig.Module.Root_Gui as Root_Gui
import YSRig.Module.Spine_Gui as Spine_Gui
import YSRig.Module.NeckFK_Gui as NeckFK_Gui
import YSRig.Module.ArmIKFK_Gui as ArmIKFK_Gui
import YSRig.Module.LegIKFK_Gui as LegIKFK_Gui
import YSRig.Module.FingerFK_Gui as FingerFK_Gui
import YSRig.YSRemoveRig as YSRemoveRig
import YSRig.YSEditLook as YSEditLook
import YSRig.YSLocator as YSLocator
import YSRig.SetUpMixamoChr as SetUpMixamoChr
import YSRig.Settings as Settings
import YSRig.YSHideUtilityNode as YSHideUtilityNode
reload(YSCreateController)
reload(SimpleFK_Gui)
reload(Root_Gui)
reload(Spine_Gui)
reload(NeckFK_Gui)
reload(ArmIKFK_Gui)
reload(LegIKFK_Gui)
reload(FingerFK_Gui)
reload(YSRemoveRig)
reload(YSEditLook)
reload(YSLocator)
reload(SetUpMixamoChr)
reload(Settings)
reload(YSHideUtilityNode)

MAINWINDOW = mel.eval('$tmpVar=$gMainWindow')
ITEM = "YSRig_Item"

if cmds.menu(ITEM, exists=True):
    cmds.deleteUI(ITEM)

cmds.menu(ITEM, parent=MAINWINDOW, tearOff=True, label="YSRig")

cmds.menuItem(parent=ITEM, label="YSRig Setting", command=lambda *args: Settings.show_Gui())
cmds.menuItem(parent=ITEM, label="Setup Mixamo Character", command=lambda *args: SetUpMixamoChr.main())
cmds.menuItem(parent=ITEM, label="Create Controller Shape", command=lambda *args: YSCreateController.show_Gui())

cmds.menuItem(parent=ITEM, label="Module", divider=True)

cmds.menuItem(parent=ITEM, label="Root", command=lambda *args: Root_Gui.show_Gui())
cmds.menuItem(parent=ITEM, label="Simple FK", command=lambda *args: SimpleFK_Gui.show_Gui())
cmds.menuItem(parent=ITEM, label="Spine", command=lambda *args: Spine_Gui.show_Gui())
cmds.menuItem(parent=ITEM, label="Neck FK", command=lambda *args: NeckFK_Gui.show_Gui())
cmds.menuItem(parent=ITEM, label="Arm IKFK", command=lambda *args: ArmIKFK_Gui.show_Gui())
cmds.menuItem(parent=ITEM, label="Leg IKFK", command=lambda *args: LegIKFK_Gui.show_Gui())
cmds.menuItem(parent=ITEM, label="Finger FK", command=lambda *args: FingerFK_Gui.show_Gui())

cmds.menuItem(parent=ITEM, label="Edit", divider=True)

cmds.menuItem(parent=ITEM, label="Remove Rig", command=lambda *args: YSRemoveRig.show_Gui())
cmds.menuItem(parent=ITEM, label="Edit Look", command=lambda *args: YSEditLook.show_Gui())

cmds.menuItem(parent=ITEM, label="Locator", divider=True)

cmds.menuItem(parent=ITEM, label="Create Locator", command=lambda *args: YSLocator.RigLocator())
cmds.menuItem(parent=ITEM, label="Distribute Locator", command=lambda *args: YSLocator.DistributeShape())
cmds.menuItem(parent=ITEM, label="Remove Locator", command=lambda *args: YSLocator.ShapeDelete())
cmds.menuItem(parent=ITEM, label="Hide UtilityNode", command=lambda *args: YSHideUtilityNode.show_Gui())