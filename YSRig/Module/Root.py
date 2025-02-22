import maya.cmds as cmds
import importlib
import YSRig.YSRig as YSRig
import YSRig.YSConnect as YSConnect
importlib.reload(YSRig)
importlib.reload(YSConnect)

def main(jt_list, sr, scale=1):
    ex = "%s_Ctrl_Grp"%("Root")
    if not len(jt_list) == 2 or cmds.objExists(ex):
        cmds.inViewMessage(amg="Error !!", pos='topCenter', fade=True)
        return
    
    proxy_list = YSRig.CopyAndReplace(jt_list, [sr[0], "Proxy_"])
    ct_hips = YSRig.CopyAndReplace([jt_list[1]], sr)
    cv = YSRig.CreateCV(shape="cube", name="curve")
    YSRig.InsertCV(cv, ct_hips, jt_list[1], scale * 30, length_scale=-1, fit_jt=True)
    ct_list = YSRig.CreateRootCtrl(jt_list, sr, scale=scale)
    group = YSRig.GroupNode("Root", jt_list[1], children=[proxy_list[0], ct_list[0]])
    ctrl_group = cmds.createNode("transform", name="Rig_Grp")
    cmds.parent(group, ctrl_group)
    root_m = cmds.duplicate(ct_list[0], po=True, name="Root_Matrix")[0]
    torso_m = cmds.duplicate(ct_list[1], po=True, name="Torso_Matrix")[0]
    cmds.parent(root_m, ct_list[0])
    cmds.parent(ct_hips, ct_list[1])
    cmds.parent(torso_m, ct_list[1])
    YSConnect.ConnectJointMatrix(ct_list[0], proxy_list[0], type="Local")
    YSConnect.ConnectJointMatrix(ct_hips[0], proxy_list[1], type="Local")
    YSConnect.AllConnectAttr(proxy_list[0], jt_list[0])
    YSConnect.AllConnectAttr(proxy_list[1], jt_list[1])
    
    YSRig.LockHideAttr(ct_list, sc=True)
    YSRig.LockHideAttr(ct_hips, sc=True, tl=True)
    YSRig.HideShapeChannel(ct_list)
    YSRig.HideShapeChannel(ct_hips)

    YSConnect.ConnectInfo(group, "joint", jt_list)
    YSConnect.ConnectInfo(group, "Ctrl", ct_list + ct_hips)
    cmds.inViewMessage(amg="Success !!", pos='midCenter', fade=True)