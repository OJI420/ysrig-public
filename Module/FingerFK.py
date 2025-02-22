import maya.cmds as cmds
import importlib
import YSRig.YSRig as YSRig
import YSRig.YSConnect as YSConnect
importlib.reload(YSRig)
importlib.reload(YSConnect)

def main(part, jt_list, sr, scale=1, shape="cube", cnnect="Local", all_axis="Z+"):
    ex = "%s_Ctrl_Grp"%(part)
    if not jt_list or not cmds.objExists("Rig_Grp") or cmds.objExists(ex) or len(jt_list) > 4:
        cmds.inViewMessage(amg="Error !!", pos='topCenter', fade=True)
        return
    
    proxy_list = YSRig.CopyAndReplace(jt_list, [sr[0], "Proxy_"])
    ctrl_list = YSRig.CopyAndReplace(jt_list, sr, cgb=True)
    space = YSRig.InsertSpaceList(ctrl_list, all=False)
    group = YSRig.GroupNode(part, jt_list[0], children=[proxy_list[0], space[0]])
    width = YSRig.Getwidth(jt_list[0]) * scale * 0.5
    for i, ct in enumerate(ctrl_list):
        cv = YSRig.CreateCV(shape=shape)
        YSRig.InsertCV(cv, ct, jt_list[i], width)
        YSConnect.AllConnectAttr(proxy_list[i], jt_list[i])
        YSConnect.ConnectMatrix(ct, proxy_list[i], type=cnnect, rt=True)

    length = abs(cmds.getAttr("%s.translateX"%(jt_list[1])))
    all = YSRig.CreateCV(shape="roll_c", name="Ctrl_%s_All"%(part))
    cmds.parent(all, jt_list[0])
    cmds.makeIdentity(all)
    roll = 0
    if all_axis == "Z+":
        roll = 90
    elif all_axis == "Y-":
        roll = 180
    elif all_axis == "Z-":
        roll = 270
    cmds.setAttr("%s.rotateX"%(all), roll)
    cmds.setAttr("%s.scale"%(all), length * 0.3, length * 0.3, length * 0.3)
    cmds.makeIdentity(all, a=True)
    all_axis, all_sign = all_axis[0], all_axis[1]
    all_sign_num = 1
    if all_sign == "-":
        all_sign_num *= -1
    cmds.setAttr("%s.translate%s"%(all, all_axis), length * all_sign_num)
    cmds.makeIdentity(all, a=True)
    cmds.parent(all, group)
    all_space = YSRig.InsertSpace(all)
    cmds.makeIdentity(all_space, a=True, t=True, r=False, s=True)
    
    roll_axis = "Z"
    if all_axis == "Z": 
        roll_axis = "Y"

    cmds.addAttr(all, ln="positiveWeight", at="double3", k=True)
    cmds.addAttr(all, ln="positiveWeight1", at="double", p="positiveWeight", dv=100, k=True)
    cmds.addAttr(all, ln="positiveWeight2", at="double", p="positiveWeight", dv=100, k=True)
    cmds.addAttr(all, ln="positiveWeight3", at="double", p="positiveWeight", dv=100, k=True)

    cmds.addAttr(all, ln="negativeWeight", at="double3", k=True)
    cmds.addAttr(all, ln="negativeWeight1", at="double", p="negativeWeight", dv=100, k=True)
    cmds.addAttr(all, ln="negativeWeight2", at="double", p="negativeWeight", dv=100, k=True)
    cmds.addAttr(all, ln="negativeWeight3", at="double", p="negativeWeight", dv=100, k=True)

    axis = "XYZ"

    cd = cmds.createNode("condition", name="Cd_%s"%(all))
    md1 = cmds.createNode("multiplyDivide", name="Md_01_%s"%(all))
    md2 = cmds.createNode("multiplyDivide", name="Md_02_%s"%(all))
    cmds.setAttr("%s.operation"%(cd), 4)
    cmds.setAttr("%s.input1"%(md1), 0.01, 0.01, 0.01)

    cmds.connectAttr("%s.positiveWeight"%(all), "%s.colorIfFalse"%(cd))
    cmds.connectAttr("%s.negativeWeight"%(all), "%s.colorIfTrue"%(cd))
    cmds.connectAttr("%s.rotate%s"%(all, roll_axis), "%s.firstTerm"%(cd))

    cmds.connectAttr("%s.outColor"%(cd), "%s.input2"%(md1))
    cmds.connectAttr("%s.output"%(md1), "%s.input2"%(md2))

    for i, s in enumerate(space):
        cmds.connectAttr("%s.rotate%s"%(all, roll_axis), "%s.input1%s"%(md2, axis[i]))
        cmds.connectAttr("%s.output%s"%(md2, axis[i]), "%s.rotate%s"%(s, roll_axis))

    cmds.setAttr("%s.rotate%s"%(all, all_axis[0]), l=True, c=False, k=False)
    cmds.setAttr("%s.rotateX"%(all), l=True, c=False, k=False)

    cmds.parent(group, "Rig_Grp")

    YSRig.LockHideAttr(ctrl_list, sc=True, tl=True)
    YSRig.LockHideAttr(all, sc=True, tl=True)
    YSRig.HideShapeChannel(ctrl_list + [all])

    YSConnect.ConnectInfo(group, "joint", jt_list)
    YSConnect.ConnectInfo(group, "Ctrl", ctrl_list + [all])
    cmds.inViewMessage(amg="Success !!", pos='midCenter', fade=True)