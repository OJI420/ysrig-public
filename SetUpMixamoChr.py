import maya.cmds as cmds
import maya.mel as mel
import YSRig.YSConnect as YSConnect

def main():
    """ Base Joint """
    mjt_list = cmds.ls(sl=True, dag=True)
    root = cmds.joint(None, name="Root")
    cmds.parent(mjt_list[0], root)
    mjt_list = [root] + mjt_list

    """ Delete Anim """
    for part_root in cmds.ls(mjt_list[0], dag=True):
        mel.eval('cutKey -cl -t ":" -f ":" -at "tx" -at "ty" -at "tz" -at "rx" -at "ry" -at "rz" %s;'%(part_root))
    
    """ Copy Joints """
    jt_list = cmds.duplicate(mjt_list, po=True, rc=True)
    jt_list = [cmds.rename(jt_list[i], "JT_%s"%(jt))for i, jt in enumerate(mjt_list)]

    for i, part_root in enumerate(jt_list):
        try:
            cmds.setAttr("%s.liw"%(part_root), l=True, k=False, cb=False)
        except:
            pass
        cmds.delete(part_root, ch=True)
        cmds.makeIdentity(part_root, a=True)
        if "Left" in part_root:
            part_root = cmds.rename(part_root, part_root.replace("Left", "L_"))
        if "Left_" in part_root:
            part_root = cmds.rename(part_root, part_root.replace("Left_", "L_"))
        if "Right" in part_root:
            part_root = cmds.rename(part_root, part_root.replace("Right", "R_"))
        if "Right_" in part_root:
            part_root = cmds.rename(part_root, part_root.replace("Right_", "R_"))
        if "Thumb" in part_root:
            part_root = cmds.rename(part_root, part_root.replace("HandThumb", "Thumb"))
        if "Index" in part_root:
            part_root = cmds.rename(part_root, part_root.replace("HandIndex", "Index"))
        if "Middle" in part_root:
            part_root = cmds.rename(part_root, part_root.replace("HandMiddle", "Middle"))
        if "Ring" in part_root:
            part_root = cmds.rename(part_root, part_root.replace("HandRing", "Ring"))
        if "Pinky" in part_root:
            part_root = cmds.rename(part_root, part_root.replace("HandPinky", "Pinky"))
        jt_list[i] = part_root

    oj_list = []
    for jt in jt_list[1:]:
        if not len(cmds.listRelatives(jt, c=True) or []) == 1:
            continue
        cj = cmds.listRelatives(jt, c=True)[0]
        tl = cmds.getAttr("%s.translate"%(cj))[0]
        if abs(tl[0]) > abs(tl[1]):
            oj_list.append(jt)

    parent_list = []
    for i, jt in enumerate(jt_list[1:]):
        parent_list.append(cmds.listRelatives(jt, p=True)[0])
        cmds.parent(jt, w=True)

    for i, jt in enumerate(jt_list[1:]):
        rot = True
        for oj in oj_list:
            if oj == jt:
                print(jt)
                rot = False
        if rot:
            cmds.rotate(90, jt, z=True)
            if "Thumb" in jt:
                cmds.rotate(90, jt, x=True)

    for i, jt in enumerate(jt_list[1:]):
        cmds.makeIdentity(jt, a=True)
        cmds.parent(jt, parent_list[i])

    for i, jt in enumerate(jt_list[1:]):
        if not cmds.listRelatives(jt, c=True):
            cmds.setAttr("%s.jointOrient"%(jt), 0, 0, 0)

    cmds.setAttr("JT_L_ForeArm.preferredAngle", 0, 0, 90)
    cmds.setAttr("JT_R_ForeArm.preferredAngle", 0, 0, -90)
    cmds.setAttr("JT_L_Leg.preferredAngle", 0, 90, 0)
    cmds.setAttr("JT_R_Leg.preferredAngle", 0, 90, 0)
    cmds.setAttr("JT_L_UpLeg.preferredAngle", 0, 0, 0)
    cmds.setAttr("JT_R_UpLeg.preferredAngle", 0, 0, 0)

    for m, y in zip(mjt_list, jt_list):
        YSConnect.ConnectJointMatrix(y, m, type="World", connect=True)