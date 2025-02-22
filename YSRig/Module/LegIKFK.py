import maya.cmds as cmds
import importlib
import YSRig.YSRig as YSRig
import YSRig.YSConnect as YSConnect
importlib.reload(YSRig)
importlib.reload(YSConnect)

def main(part, jt_list, sr, fk_scale=1, fk_shape="cube", ikh_shape="foot", pv_shape="sphere", ik_scale=1, ik_length=1, pv_axis="Z+", up_axis="Z+", out_axis="Y+", rev_scale=1):
    ex = "%s_Ctrl_Grp"%(part)
    if not len(jt_list) == 5 or not cmds.objExists("Rig_Grp") or cmds.objExists(ex):
        cmds.inViewMessage(amg="Error !!", pos='topCenter', fade=True)
        return

    proxy_list = YSRig.CopyAndReplace(jt_list, [sr[0], "Proxy_"])
    fk_ctrl_list = YSRig.CopyAndReplace(jt_list, sr, cgb=True)
    ik_jt_list = YSRig.CopyAndReplace(jt_list, [sr[0], "IK_"])

    group = YSRig.GroupNode(part, jt_list[0], children=[proxy_list[0], fk_ctrl_list[0], ik_jt_list[0]])
    fk_width = YSRig.Getwidth(jt_list[0]) * fk_scale * 0.35

    """ FK Setup"""
    YSRig.SetWorldRotate(fk_ctrl_list[2])
    for i, ct in enumerate(fk_ctrl_list):
        if i == 2:
            cv = YSRig.CreateCV(shape="center_cube")
            shape = YSRig.InsertCV(cv, ct, jt_list[i], fk_width * 0.85, fit_jt=False)
        else:
            cv = YSRig.CreateCV(shape=fk_shape)
            length_scale = 0.9
            if i == 1:
                length_scale = 0.7
            elif i > 2:
                fk_width *= 0.8
            shape = YSRig.InsertCV(cv, ct, jt_list[i], fk_width, length_scale=length_scale)
        if i > 2:
            YSRig.MatchBottom(shape)

    """ IK Setup"""
    foot_size = YSRig.GetSumlength(ik_jt_list[2:])
    ik_hd, ctrl_hd, ctrl_pv = YSRig.CreateLegIK(part, ik_jt_list, ikh_shape, pv_shape, ik_scale, ik_length, pv_axis, foot_size)
    rev_ik_hd = YSRig.CreateReverseFootIK(ik_jt_list[2:])
    ik_toe = cmds.createNode("transform", name=jt_list[3].replace(sr[0], "Ctrl_IK_"))
    cmds.matchTransform(ik_toe, jt_list[3])
    ik_toe_space = YSRig.InsertSpace(ik_toe)
    ik_toe_cn = YSRig.InsertSpace(ik_toe, name="Connect")
    cv = YSRig.CreateCV(shape=fk_shape)
    shape = YSRig.InsertCV(cv, ik_toe, jt_list[3], fk_width)
    YSRig.MatchBottom(shape)

    jt_axis = 1
    if cmds.getAttr("%s.translateX"%(jt_list[3])) < 0:
        jt_axis = -1

    out_axis, out_sign = out_axis[0], out_axis[1]
    out_sign_num = 1
    if out_sign == "-":
        out_sign_num *= -1

    up_axis, up_sign = up_axis[0], up_axis[1]
    up_sign_num = 1
    if up_sign == "-":
        up_sign_num *= -1

    """ Reverse Foot Setup"""
    ctrl_heel = YSRig.CreateReverseFootCtrl(jt_list[3], "X", -1 * jt_axis * 1.75, foot_size, bottom=True, scale=rev_scale, name="Ctrl_%s_Rev_Heel"%(part))
    ctrl_out = YSRig.CreateReverseFootCtrl(jt_list[3], out_axis, 1 * out_sign_num * 0.6, foot_size, bottom=True, scale=rev_scale, name="Ctrl_%s_Rev_Outside"%(part))
    ctrl_in = YSRig.CreateReverseFootCtrl(jt_list[3], out_axis, -1 * out_sign_num * 0.6, foot_size, bottom=True, scale=rev_scale, name="Ctrl_%s_Rev_Inside"%(part))
    ctrl_tiptoe = YSRig.CreateReverseFootCtrl(jt_list[3], "X", 1 * jt_axis, foot_size, bottom=True, scale=rev_scale, name="Ctrl_%s_Rev_Tiptoe"%(part))
    ctrl_toe = YSRig.CreateReverseFootCtrl(jt_list[3], up_axis, 1 * up_sign_num, foot_size, bottom=False, scale=rev_scale, name="Ctrl_%s_Rev_Toe"%(part), target=ctrl_tiptoe[2])

    rev_grp = YSRig.InsertSpace(ctrl_hd)
    rev_grp = cmds.rename(rev_grp, "%s_ReverseFoot_Grp"%(part))
    ik_space = YSRig.InsertSpace(ctrl_hd)

    cmds.parent(rev_ik_hd, ik_toe)
    cmds.parent(ik_hd, ctrl_toe[2])
    cmds.parent(rev_grp, group)

    cmds.parent(ctrl_toe[0], ctrl_tiptoe[2])
    cmds.parent(ctrl_tiptoe[0], ctrl_in[2])
    cmds.parent(ctrl_in[0], ctrl_out[2])
    cmds.parent(ctrl_out[0], ctrl_heel[2])
    cmds.parent(ctrl_heel[0], ctrl_hd)
    cmds.parent(ctrl_pv, ctrl_hd)
    pv_space = YSRig.InsertSpace(ctrl_pv)
    
    cmds.makeIdentity(pv_space, apply=True)
    cmds.parent(ik_toe_space, ctrl_tiptoe[2])
    cmds.makeIdentity(ik_toe_space, apply=True, t=True, r=False, s=True)
    pb = []
    for i, ct in enumerate(fk_ctrl_list):
        YSConnect.AllConnectAttr(proxy_list[i], jt_list[i])
        pb.append(YSConnect.ConnectPairBlend(ik_jt_list[i], ct, proxy_list[i]))
    YSConnect.ConnectWeight(group, "IKFK", "long", pb)

    YSConnect.connectVisibility("%s.IKFK"%(group), fk_ctrl_list, [ctrl_hd, ctrl_pv])
    
    YSConnect.ConnectWorldMatrix(ik_space, "IK_WL", group, "Root_Matrix", inv=True)
    YSConnect.ConnectWorldMatrix(pv_space, "PV_WL", group, "Root_Matrix", inv=True)

    cmds.setAttr("%s.IKFK"%(group), 0)
    cmds.setAttr("%s.IK_WL"%(group), 0)
    cmds.setAttr("%s.PV_WL"%(group), 0)

    """ Reverse Foot All Controller"""
    all_ctrl = YSRig.CreateCV(shape="octahedron")
    all_ctrl = cmds.rename(all_ctrl, "Ctrl_%s_ReverseFoot_All"%(part))
    cmds.parent(all_ctrl, ctrl_tiptoe[2])
    cmds.matchTransform(all_ctrl, ctrl_tiptoe[2])
    cmds.makeIdentity(all_ctrl, a=True)
    all_len = foot_size * rev_scale * 0.6
    cmds.setAttr("%s.translateX"%(all_ctrl), all_len * -0.8)
    cmds.setAttr("%s.translateY"%(all_ctrl), all_len * 0.5)
    all_scale = all_len * rev_scale * 0.15
    cmds.scale(all_scale, all_scale, all_scale, all_ctrl, cs=True, r=True)
    cmds.parent(all_ctrl, w=True)
    cmds.makeIdentity(all_ctrl, a=True, t=True, r=False, s=True)
    all_space = YSRig.InsertSpace(all_ctrl)
    all_cv = cmds.listRelatives(all_ctrl, s=True)[0]
    cvnum = cmds.getAttr("%s.controlPoints"%(all_cv), size=True)
    cmds.move(0, "%s.cv[%d]"%(all_cv, cvnum), "%s.cv[%d]"%(all_cv, cvnum), y=True, ws=True, os=True, wd=True)
    cmds.move(0, "%s.scalePivot"%(all_ctrl), "%s.rotatePivot"%(all_ctrl), y=True, a=True, cs=True)
    cmds.parent(all_space, ctrl_hd)

    # out in side
    tmp_aim = cmds.aimConstraint(ctrl_out[2], all_ctrl, o=[0, 0, 0], w=1, aim=[1, 0, 0], u=[0, 1, 0], wut="vector", wu=[0, 1, 0])
    sign = cmds.getAttr("%s.rotateY"%(all_ctrl))
    cmds.delete(tmp_aim)
    cmds.setAttr("%s.rotateY"%(all_ctrl), 0)
    sign = sign / abs(sign) * -1
    for ct in [ctrl_out[1], ctrl_in[1]]:
        fm = cmds.createNode("floatMath", name="Fm_%s"%(ct))
        cd = cmds.createNode("condition", name="Cd_%s"%(ct))
        cmds.setAttr("%s.operation"%(fm), 2)
        cmds.setAttr("%s.floatB"%(fm), sign)
        cmds.setAttr("%s.operation"%(cd), 3)
        cmds.setAttr("%s.colorIfFalseR"%(cd), 0)
        cmds.connectAttr("%s.rotateX"%(all_ctrl), "%s.floatA"%(fm))
        cmds.connectAttr("%s.outFloat"%(fm), "%s.colorIfTrueR"%(cd))
        cmds.connectAttr("%s.outFloat"%(fm), "%s.firstTerm"%(cd))
        cmds.connectAttr("%s.outColorR"%(cd), "%s.rotateZ"%(ct))
        sign *= -1
    cmds.addAttr(all_ctrl, ln="toeBendThreshold", at="double", min=0, max=180, dv=0, k=True)
    cmds.addAttr(all_ctrl, ln="toeReverseThreshold", at="double", min=0, max=180, dv=40, k=True)

    # heel
    cn = ctrl_heel[1]
    fm = cmds.createNode("floatMath", name="Fm_%s"%(cn))
    cd = cmds.createNode("condition", name="Cd_%s"%(cn))
    cmds.setAttr("%s.operation"%(fm), 2)
    cmds.setAttr("%s.floatB"%(fm), -1)
    cmds.setAttr("%s.operation"%(cd), 4)
    cmds.setAttr("%s.colorIfFalseR"%(cd), 0)
    cmds.connectAttr("%s.rotateZ"%(all_ctrl), "%s.colorIfTrueR"%(cd))
    cmds.connectAttr("%s.rotateZ"%(all_ctrl), "%s.firstTerm"%(cd))
    cmds.connectAttr("%s.outColorR"%(cd), "%s.floatA"%(fm))
    cmds.connectAttr("%s.outFloat"%(fm), "%s.rotateZ"%(cn))

    # toe
    cn = ik_toe_cn
    cd1 = cmds.createNode("condition", name="Cd_%s_01"%(cn))
    cd2 = cmds.createNode("condition", name="Cd_%s_02"%(cn))
    cmds.setAttr("%s.operation"%(cd1), 4)
    cmds.setAttr("%s.operation"%(cd2), 3)
    cmds.setAttr("%s.colorIfFalseR"%(cd2), 0)
    cmds.connectAttr("%s.rotateZ"%(all_ctrl), "%s.colorIfTrueR"%(cd1))
    cmds.connectAttr("%s.rotateZ"%(all_ctrl), "%s.firstTerm"%(cd1))
    cmds.connectAttr("%s.toeBendThreshold"%(all_ctrl), "%s.colorIfFalseR"%(cd1))
    cmds.connectAttr("%s.toeBendThreshold"%(all_ctrl), "%s.secondTerm"%(cd1))
    cmds.connectAttr("%s.outColorR"%(cd1), "%s.colorIfTrueR"%(cd2))
    cmds.connectAttr("%s.outColorR"%(cd1), "%s.firstTerm"%(cd2))
    cmds.connectAttr("%s.outColorR"%(cd2), "%s.rotate%s"%(cn, out_axis))

    # Rev Toe
    cn = ctrl_toe[1]
    cd1 = cmds.createNode("condition", name="Cd_%s_01"%(cn))
    cd2 = cmds.createNode("condition", name="Cd_%s_02"%(cn))
    cd3 = cmds.createNode("condition", name="Cd_%s_03"%(cn))
    fm1 = cmds.createNode("floatMath", name="Fm_%s_01"%(cn))
    fm2 = cmds.createNode("floatMath", name="Fm_%s_02"%(cn))
    fm3 = cmds.createNode("floatMath", name="Fm_%s_03"%(cn))
    fm4 = cmds.createNode("floatMath", name="Fm_%s_04"%(cn))
    cmds.setAttr("%s.operation"%(cd1), 3)
    cmds.setAttr("%s.operation"%(cd2), 4)
    cmds.setAttr("%s.operation"%(cd3), 3)
    cmds.setAttr("%s.colorIfFalseR"%(cd1), 0)
    cmds.setAttr("%s.colorIfFalseR"%(cd3), 0)
    cmds.setAttr("%s.operation"%(fm1), 1)
    cmds.setAttr("%s.operation"%(fm2), 1)
    cmds.setAttr("%s.operation"%(fm3), 1)
    cmds.connectAttr("%s.rotateZ"%(all_ctrl), "%s.floatA"%(fm1))
    cmds.connectAttr("%s.toeBendThreshold"%(all_ctrl), "%s.floatB"%(fm1))
    cmds.connectAttr("%s.toeReverseThreshold"%(all_ctrl), "%s.floatA"%(fm2))
    cmds.connectAttr("%s.toeBendThreshold"%(all_ctrl), "%s.floatB"%(fm2))
    cmds.connectAttr("%s.outFloat"%(fm1), "%s.colorIfTrueR"%(cd1))
    cmds.connectAttr("%s.rotateZ"%(all_ctrl), "%s.firstTerm"%(cd1))
    cmds.connectAttr("%s.toeBendThreshold"%(all_ctrl), "%s.secondTerm"%(cd1))
    cmds.connectAttr("%s.outColorR"%(cd1), "%s.floatB"%(fm3))
    cmds.connectAttr("%s.outFloat"%(fm2), "%s.floatA"%(fm3))
    cmds.connectAttr("%s.outFloat"%(fm3), "%s.floatA"%(fm4))
    cmds.connectAttr("%s.outFloat"%(fm2), "%s.floatB"%(fm4))

    cmds.connectAttr("%s.outFloat"%(fm4), "%s.colorIfFalseR"%(cd2))
    cmds.connectAttr("%s.rotateZ"%(all_ctrl), "%s.firstTerm"%(cd2))
    cmds.connectAttr("%s.toeReverseThreshold"%(all_ctrl), "%s.secondTerm"%(cd2))
    cmds.connectAttr("%s.outColorR"%(cd1), "%s.colorIfTrueR"%(cd2))

    cmds.connectAttr("%s.outColorR"%(cd2), "%s.colorIfTrueR"%(cd3))
    cmds.connectAttr("%s.outColorR"%(cd2), "%s.firstTerm"%(cd3))
    cmds.connectAttr("%s.outColorR"%(cd3), "%s.rotateZ"%(cn))

    # Tiptoe
    cn = ctrl_tiptoe[1]
    fm = cmds.createNode("floatMath", name="Fm_%s"%(cn))
    cd = cmds.createNode("condition", name="Cd_%s"%(cn))
    cmds.setAttr("%s.operation"%(fm), 1)
    cmds.setAttr("%s.operation"%(cd), 3)
    cmds.setAttr("%s.colorIfFalseR"%(cd), 0)
    cmds.connectAttr("%s.rotateZ"%(all_ctrl), "%s.floatA"%(fm))
    cmds.connectAttr("%s.toeReverseThreshold"%(all_ctrl), "%s.floatB"%(fm))
    cmds.connectAttr("%s.outFloat"%(fm), "%s.colorIfTrueR"%(cd))
    cmds.connectAttr("%s.rotateZ"%(all_ctrl), "%s.firstTerm"%(cd))
    cmds.connectAttr("%s.toeReverseThreshold"%(all_ctrl), "%s.secondTerm"%(cd))
    cmds.connectAttr("%s.outColorR"%(cd), "%s.rotateZ"%(cn))
    cmds.setAttr("%s.rotateY"%(all_ctrl), l=True, c=False, k=False)
    
    foot_ctrl_list = [ctrl_heel[2], ctrl_out[2], ctrl_in[2], ctrl_tiptoe[2], ctrl_toe[2], ik_toe, all_ctrl]

    cmds.parent(group, "Rig_Grp")

    rz=True
    ry=True
    if pv_axis[0] == "Z":
        ry=False
    elif pv_axis[0] == "Y":
        rz=False

    YSRig.LockHideAttr(fk_ctrl_list + foot_ctrl_list, sc=True, tl=True)
    YSRig.LockHideAttr(fk_ctrl_list[1], sc=True, tl=True, rt=True, ry=ry, rz=rz)
    YSRig.LockHideAttr(ctrl_hd, sc=True)
    YSRig.LockHideAttr(ctrl_pv, sc=True, rt=True)
    YSRig.HideShapeChannel(fk_ctrl_list + [ctrl_hd, ctrl_pv] + foot_ctrl_list)

    YSConnect.ConnectInfo(group, "joint", jt_list)
    YSConnect.ConnectInfo(group, "Ctrl", fk_ctrl_list + [ctrl_hd, ctrl_pv] + foot_ctrl_list)
    cmds.inViewMessage(amg="Success !!", pos='midCenter', fade=True)