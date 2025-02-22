import maya.cmds as cmds
import importlib
import YSRig.YSRig as YSRig
import YSRig.YSConnect as YSConnect
importlib.reload(YSRig)
importlib.reload(YSConnect)

def main(part, jt_list, sr, scale=1, shape="spine", cnnect="Local"):
    ex = "%s_Ctrl_Grp"%(part)
    if not jt_list or not cmds.objExists("Rig_Grp") or cmds.objExists(ex):
        cmds.inViewMessage(amg="Error !!", pos='topCenter', fade=True)
        return
    
    proxy_list = YSRig.CopyAndReplace(jt_list, [sr[0], "Proxy_"])
    ctrl_list = YSRig.CopyAndReplace(jt_list, sr, cgb=True)
    group = YSRig.GroupNode(part, jt_list[0], children=[proxy_list[0], ctrl_list[0]])
    cn = YSRig.InsertSpace(ctrl_list[0], name="Connect")
    width = YSRig.Getwidth(jt_list[0]) * scale * 2
    for i, ct in enumerate(ctrl_list):
        YSRig.SetWorldRotate(ct)
        cv = YSRig.CreateCV(shape=shape)
        YSRig.InsertCV(cv, ct, jt_list[i], width)
        YSConnect.AllConnectAttr(proxy_list[i], jt_list[i])
        YSConnect.ConnectJointMatrix(ct, proxy_list[i], type="Local")
    YSConnect.ConnectJointMatrix("Torso_Matrix", cn, type="Local")

    cmds.parent(group, "Rig_Grp")

    YSRig.LockHideAttr(ctrl_list, sc=True, tl=True)
    YSRig.HideShapeChannel(ctrl_list)
    
    YSConnect.ConnectInfo(group, "joint", jt_list)
    YSConnect.ConnectInfo(group, "Ctrl", ctrl_list)
    cmds.inViewMessage(amg="Success !!", pos='midCenter', fade=True)