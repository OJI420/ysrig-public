import maya.cmds as cmds
import importlib
import YSRig.YSRig as YSRig
import YSRig.YSConnect as YSConnect
importlib.reload(YSRig)
importlib.reload(YSConnect)

def main(part, jt_list, sr, scale=1, handScale=1, shape="cube", handShape="hand", pvAxis="Z-", hds="locator", pvs="sphere", length=1, ik_scale=1):
    ex = "%s_Ctrl_Grp"%(part)
    if not len(jt_list) == 3 or not cmds.objExists("Rig_Grp") or cmds.objExists(ex):
        cmds.inViewMessage(amg="Error !!", pos='topCenter', fade=True)
        return

    proxy_list = YSRig.CopyAndReplace(jt_list, [sr[0], "Proxy_"])
    fk_ctrl_list = YSRig.CopyAndReplace(jt_list, sr)
    hand_ctrl = fk_ctrl_list[2]
    fk_ctrl_list = [fk_ctrl_list[0], fk_ctrl_list[1]]
    ik_jt_list = YSRig.CopyAndReplace(jt_list, [sr[0], "IK_"])
    group = YSRig.GroupNode(part, jt_list[0], children=[proxy_list[0], fk_ctrl_list[0], ik_jt_list[0]])

    width = YSRig.Getwidth(jt_list[0]) * scale / 2

    pb = [None, None]
    for i, ct in enumerate(fk_ctrl_list):
        cv = YSRig.CreateCV(shape=shape)
        YSRig.InsertCV(cv, ct, jt_list[i], width)
        YSConnect.AllConnectAttr(proxy_list[i], jt_list[i])
        pb[i] = YSConnect.ConnectPairBlend(ik_jt_list[i], ct, proxy_list[i])
    cmds.parent(hand_ctrl, proxy_list[1])
    hand_space = YSRig.InsertSpace(hand_ctrl)
    YSConnect.ConnectWeight(group, "IKFK", "long", pb)
    cv = YSRig.CreateCV(shape=handShape)
    YSRig.InsertHandCV(cv, hand_ctrl, jt_list[2], handScale, type=handShape)
    YSConnect.ConnectMatrix(hand_ctrl, proxy_list[2], type="Local", rt=True)
    YSConnect.AllConnectAttr(proxy_list[2], jt_list[2])

    hd, pv = YSRig.CreateIK(part, ik_jt_list, hds, pvs, ik_scale, length, pvAxis)
    cmds.parent(pv, hd)
    cmds.parent(hd, group)
    hd_space = YSRig.InsertSpace(hd)
    hd_connect = YSRig.InsertSpace(hd, name="Connect")
    pv_space = YSRig.InsertSpace(pv)
    YSConnect.connectVisibility("%s.IKFK"%(group), fk_ctrl_list, [hd, pv])
    
    YSConnect.ConnectWorldMatrix(hand_space, "Hand_WL", group, "Root_Matrix", tl=False, inv=True)
    YSConnect.ConnectWorldMatrix(hd_connect, "IK_WL", group, "Root_Matrix", inv=True)
    YSConnect.ConnectWorldMatrix(pv_space, "PV_WL", group, "Root_Matrix", inv=True)

    cmds.setAttr("%s.IKFK"%(group), 0)
    cmds.setAttr("%s.Hand_WL"%(group), 0)
    cmds.setAttr("%s.IK_WL"%(group), 0)
    cmds.setAttr("%s.PV_WL"%(group), 0)

    cmds.parent(group, "Rig_Grp")

    rz=True
    ry=True
    if pvAxis[0] == "Z":
        ry=False
    elif pvAxis[0] == "Y":
        rz=False

    YSRig.LockHideAttr(fk_ctrl_list + [hand_ctrl], sc=True, tl=True)
    YSRig.LockHideAttr(fk_ctrl_list[1], sc=True, tl=True, rt=True, ry=ry, rz=rz)
    YSRig.LockHideAttr(hd, sc=True)
    YSRig.LockHideAttr(pv, sc=True, rt=True)
    YSRig.HideShapeChannel(fk_ctrl_list + [hd, pv] + [hand_ctrl])

    YSConnect.ConnectInfo(group, "joint", jt_list)
    YSConnect.ConnectInfo(group, "Ctrl", fk_ctrl_list + [hd, pv] + [hand_ctrl])
    cmds.inViewMessage(amg="Success !!", pos='midCenter', fade=True)