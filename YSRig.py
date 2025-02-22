import os
import json
import maya.cmds as cmds

def InsertSpace(node, name="Space"):
    space = cmds.duplicate(node, po=True, name="%s_%s"%(node, name))[0]
    
    cmds.parent(node, space)
    
    cmds.setAttr("%s.translate"%(node), 0, 0, 0)
    cmds.setAttr("%s.rotate"%(node), 0, 0, 0)
    cmds.setAttr("%s.scale"%(node), 1, 1, 1)
    cmds.setAttr("%s.shear"%(node), 0, 0, 0)
    
    if cmds.nodeType(node) == "joint":
        cmds.setAttr("%s.jointOrient"%(node), 0, 0, 0)
    return space

def InsertSpaceList(node_list, all=True):
    re_list = []
    for node in node_list:
        re_list.append(InsertSpace(node))
        if all:
            re_list.append(node)
    return re_list

def CreateCV(shape="circle", name="curve"):
    savefile = os.path.join(cmds.internalVar(userPrefDir=True), "YSRigControlShape.json")
    ld = {}
    if os.path.exists(savefile):
        with open(savefile, "r") as f:
            ld = json.load(f)
    
    cv_pos, cv_knot = ld.get("CVpoints_%s"%(shape), []), ld.get("CVknot_%s"%(shape), [])
        
    cv = cmds.curve(d=1, p=cv_pos, k=cv_knot, name=name)
    cmds.rename(cmds.listRelatives(cv, s=True)[0], "%sShape"%(cv))
    return cv

def CopyAndReplace(jt_list, sr, cgb=False):
    if cgb:
        if not cmds.listRelatives(jt_list[-1], c=True) or []:
            jt_list = jt_list[:-1]
    re_list = cmds.duplicate(jt_list, po=True, rc=True)
    re_list = [cmds.rename(re_list[i], jt.replace(sr[0], sr[1]))for i, jt in enumerate(jt_list)]
    for jt in re_list:
        cmds.setAttr("%s.drawStyle"%(jt), 2)
    return re_list

def GroupNode(part, node, children=[]):
    parent = cmds.listRelatives(node, p=True)[0]
    grp = cmds.createNode("transform", name="%s_Ctrl_Grp"%(part))
    cmds.matchTransform(grp, parent)
    if children:
        for c in children:
            cmds.parent(c, grp)
    return grp

def InsertCV(cv, ct, jt, width, length_scale=0.9, fit_jt=True):
    if fit_jt:
        child = cmds.listRelatives(jt, c=True)
        if not child:
            child = jt
        else:
            child = child[0]
        length = cmds.getAttr("%s.translateX"%(child))
        shape = cmds.listRelatives(cv, s=True)[0]
        cmds.setAttr("%s.scale"%(cv), length * length_scale, width, width)
    else:
        shape = cmds.listRelatives(cv, s=True)[0]
        cmds.setAttr("%s.scale"%(cv), width, width, width)

    cmds.makeIdentity(cv, apply=True)
    cmds.parent(shape, ct, r=True, s=True)
    cmds.delete(cv)
    if isinstance(ct, list):
        ct = ct[0]
    shape = cmds.rename(shape, "%sShape"%(ct))
    return shape

def Getwidth(jt):
    width = cmds.getAttr("%s.translateX"%(cmds.listRelatives(jt, c=True)[0]))
    return abs(width)

def CreateRootCtrl(jt_list, sr, scale=1):
    hips_name = jt_list[1].replace(sr[0], "")
    ctrl = []
    ctrl.append(CreateCV(shape="root", name=jt_list[0].replace(sr[0], sr[1])))
    ctrl.append(CreateCV(shape="torso", name=jt_list[1].replace(sr[0], sr[1]).replace(hips_name, "Torso")))
    s = []
    s.append(cmds.getAttr("%s.translateY"%(jt_list[1])) * scale / 1.5)
    s.append(s[0] / 2)
    for i, c in enumerate(ctrl):
        cmds.matchTransform(c, jt_list[i])
        cmds.scale(s[i], s[i], s[i], c)
    cmds.parent(ctrl[1], ctrl[0])
    cmds.makeIdentity(ctrl, apply=True)
    return ctrl

def InsertHandCV(cv, ct, jt, width, type="hand"):
    child = cmds.listRelatives(jt, c=True)[0]
    if not child:
        child = jt
    length = cmds.getAttr("%s.translateX"%(child))
    shape = cmds.listRelatives(cv, s=True)[0]
    if type == "hand":
        cmds.setAttr("%s.scale"%(cv), length * width * 4 , length * width * 4, length * width * 4)
    else:
        cmds.setAttr("%s.scale"%(cv), length * width * 0.4, length * width * 2.5, length * width * 2.5)
    cmds.makeIdentity(cv, apply=True)
    cmds.parent(shape, ct, r=True, s=True)
    cmds.delete(cv)
    cmds.rename(shape, "%sShape"%(ct))
    return shape

def CreateIK(part, ik_jt_list, hds, pvs, scale, length, axis):
    hd , ef = cmds.ikHandle(sj=ik_jt_list[0], ee=ik_jt_list[2], name="Ikhdl_%s"%(part))
    ctrl_hd = CreateCV(shape=hds, name="Ctrl_Ik_%s"%(part))
    ctrl_pv = CreateCV(shape=pvs, name="Ctrl_Pv_%s"%(part))
    arm_length = cmds.getAttr("%s.translateX"%(ik_jt_list[2]))
    scale = scale * arm_length * 0.5
    cmds.matchTransform(ctrl_hd, ik_jt_list[2], pos=True, rot=False, scl=False)
    cmds.matchTransform(ctrl_pv, ik_jt_list[1], pos=True, rot=False, scl=False)
    cmds.scale(scale, scale, scale, ctrl_hd)
    cmds.scale(scale * 0.3, scale * 0.3, scale * 0.3, ctrl_pv)
    tmp_jt = cmds.duplicate(ik_jt_list[1], po=True, rc=True)[0]
    cmds.matchTransform(tmp_jt, ik_jt_list[0], pos=False, rot=True, scl=False)
    cmds.parent(ctrl_pv, tmp_jt)
    axis, sign = axis[0], axis[1]
    sign_num = 1
    if sign == "-":
        sign_num = -1
    cmds.setAttr("%s.translate%s"%(tmp_jt, axis), length * abs(arm_length) * sign_num)
    cmds.parent(ctrl_pv, w=True)
    cmds.parent(hd, ctrl_hd)
    cmds.delete(tmp_jt)
    cmds.makeIdentity(ctrl_hd, apply=True)
    cmds.makeIdentity(ctrl_pv, apply=True)
    cmds.poleVectorConstraint(ctrl_pv, hd, name="Pvc_%s"%(hd))
    cmds.setAttr("%s.visibility"%(hd), 0)
    return ctrl_hd, ctrl_pv

def SetWorldRotate(node):
    tmp_node = cmds.createNode("transform", name="tmp_%s"%(node))
    child_node = cmds.listRelatives(node, c=True)
    cmds.matchTransform(tmp_node, node)
    for axis in "XYZ":
        rot = cmds.getAttr("%s.rotate%s"%(tmp_node, axis))
        rot = round(rot / 90.0) * 90
        cmds.setAttr("%s.rotate%s"%(tmp_node, axis), rot)
    try:
        for c in child_node:
            cmds.parent(c, w=True)
        cmds.matchTransform(node, tmp_node)
        cmds.makeIdentity(node, apply=True)
        for c in child_node:
            cmds.parent(c, node)
    except:
        cmds.matchTransform(node, tmp_node)
        cmds.makeIdentity(node, apply=True)
    cmds.delete(tmp_node)

def MatchBottom(shape, all=False):
    for i in range(cmds.getAttr("%s.controlPoints"%(shape), size=True)):
        pos = cmds.xform("%s.cv[%d]"%(shape, i), q=True, ws=True, translation=True)
        if all:
            cmds.move(pos[0], 0, pos[2], "%s.cv[%d]"%(shape, i), "%s.cv[%d]"%(shape, i), ws=True, os=True, wd=True)
        else:
            if pos[1] <= 0:
                cmds.move(pos[0], 0, pos[2], "%s.cv[%d]"%(shape, i), "%s.cv[%d]"%(shape, i), ws=True, os=True, wd=True)

def GetSumlength(jt_list):
    jt1 = cmds.duplicate(jt_list[0], po=True)[0]
    jt2 = cmds.joint(jt1, name="%s_2"%(jt1))
    aim = cmds.aimConstraint(jt_list[-1], jt1, offset=[0,0,0], aim=[1,0,0])
    cmds.matchTransform(jt2,jt_list[-1],  pos=True, rot=False, scl=False)
    sum = cmds.getAttr("%s.translateX"%(jt2))
    cmds.delete(jt1)
    return sum

def CreateLegIK(part, ik_jt_list, hds, pvs, scale, length, axis, foot_size):
    hd , ef = cmds.ikHandle(sj=ik_jt_list[0], ee=ik_jt_list[2], name="Ikhdl_%s"%(part))
    ctrl_hd = CreateCV(shape=hds, name="Ctrl_Ik_%s"%(part))
    ctrl_pv = CreateCV(shape=pvs, name="Ctrl_Pv_%s"%(part))
    cmds.matchTransform(ctrl_hd, ik_jt_list[2], pos=True, rot=False, scl=False)
    cmds.matchTransform(ctrl_pv, ik_jt_list[1], pos=True, rot=False, scl=False)
    tmp_aim = cmds.aimConstraint(ik_jt_list[-1], ctrl_hd, offset=[0,0,0], aim=[1,0,0])
    cmds.delete(tmp_aim)

    scale = scale * foot_size
    cmds.scale(foot_size * 1.4, scale * 0.75, scale * 0.75, ctrl_hd)
    cmds.scale(scale * 0.1, scale * 0.1, scale * 0.1, ctrl_pv)

    tmp_jt = cmds.duplicate(ik_jt_list[1], po=True, rc=True)[0]
    cmds.matchTransform(tmp_jt, ik_jt_list[0], pos=False, rot=True, scl=False)
    cmds.parent(ctrl_pv, tmp_jt)

    axis, sign = axis[0], axis[1]
    sign_num = 1
    if sign == "-":
        sign_num = -1

    cmds.setAttr("%s.translate%s"%(tmp_jt, axis), length * abs(foot_size) * sign_num * 1.5)
    cmds.parent(ctrl_pv, w=True)
    cmds.delete(tmp_jt)
    cmds.makeIdentity(ctrl_hd, apply=True)
    cmds.makeIdentity(ctrl_pv, apply=True)
    cmds.poleVectorConstraint(ctrl_pv, hd, name="Pvc_%s"%(hd))
    cmds.setAttr("%s.visibility"%(hd), 0)

    shape = cmds.listRelatives(ctrl_hd, s=True)[0]
    MatchBottom(shape, all=True)

    return hd, ctrl_hd, ctrl_pv

def CreateReverseFootIK(jt_list):
    jt_list = list(reversed(jt_list))
    hd = []
    for i, jt in enumerate(jt_list):
        if i == len(jt_list) -1:
            break
        hd.append(cmds.ikHandle(sj=jt_list[i+1], ee=jt, sol="ikSCsolver", name="Ikhd_%s"%(jt))[0])
        cmds.setAttr("%s.visibility"%(hd[i]), 0)
    return list(reversed(hd))

def CreateReverseFootCtrl(jt, axis, length, foot_size, bottom=False, scale=1, name="ctrl#", target=None):
    tmp_jt = cmds.duplicate(jt, po=True)[0]
    cmds.move(0, tmp_jt, y=True, ws=True, a=True)
    length = foot_size * length * 0.5
    scale = scale * foot_size * 0.15
    ct = CreateCV(shape="diamond")
    ct = cmds.rename(ct, name)
    cmds.rename(cmds.listRelatives(ct, s=True)[0], "%sShape"%(name))
    cmds.parent(ct, jt)
    cmds.makeIdentity(ct)
    cmds.setAttr("%s.translate%s"%(ct, axis), length)
    cmds.parent(ct, ct, w=True)
    cmds.scale(scale, scale, scale, ct)
    if bottom:
        cmds.move(0, moveY=True, a=True, ws=True)
    am = cmds.aimConstraint(tmp_jt, ct, o=[0, 0, 0], w=1, aim=[1, 0, 0], u=[0, 1, 0], wut="vector", wu=[0, 1, 0])
    if target:
        cmds.matchTransform(ct, target, pos=False, rot=True, scl=False)
        cmds.rotate(-90, ct, z=True, cs=True, r=True)
    cmds.delete(am)
    cmds.delete(tmp_jt)
    space = InsertSpace(ct)
    cn = InsertSpace(ct, name="Connect")
    cmds.makeIdentity(space, t=True, r=False, s=True, a=True)
    if bottom:
        MatchBottom(cmds.listRelatives(ct, s=True)[0], all=True)
    else:
        piv = cmds.xform(jt, q=True, ws=True, sp=True)
        cmds.move(piv[0], piv[1], piv[2], "%s.scalePivot"%(ct), "%s.rotatePivot"%(ct),  a=True)
    cmds.connectAttr("%s.rotatePivot"%(ct), "%s.rotatePivot"%(cn))
    cmds.connectAttr("%s.scalePivot"%(ct), "%s.scalePivot"%(cn))
    return [space, cn, ct]

def LockHideAttr(node_list, tl=False, rt=False, sc=False, tx=True, ty=True, tz=True, rx=True, ry=True, rz=True, sx=True, sy=True, sz=True, rd=True):
    if isinstance(node_list, str):
        node_list = [node_list]
    for node in node_list:
        if tl:
            for a1, a2 in zip("XYZ", [tx, ty, tz]):
                cmds.setAttr("%s.translate%s"%(node, a1), l=a2, k=not a2, c=not a2)
        if rt:
            for a1, a2 in zip("XYZ", [rx, ry, rz]):
                cmds.setAttr("%s.rotate%s"%(node, a1), l=a2, k=not a2, c=not a2)
        if sc:
            for a1, a2 in zip("XYZ", [sx, sy, sz]):
                cmds.setAttr("%s.scale%s"%(node, a1), l=a2, k=not a2, c=not a2)
        try:
            cmds.setAttr("%s.radi"%(node), k=rd, c=rd)
            cmds.setAttr("%s.radi"%(node), k=not rd, c=not rd)
        except:
            pass

def HideShapeChannel(node_list, hide=True):
    if isinstance(node_list, str):
        node_list = [node_list]
    for node in node_list:
        shape_list = cmds.listRelatives(node, s=True) or []
        for shape in shape_list:
            cmds.setAttr("%s.ihi" %(shape), not hide)
