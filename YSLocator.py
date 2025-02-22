import maya.cmds as cmds

def CreateLocator(name="LC"):
    lc = cmds.spaceLocator(n=name)[0]
    lc = cmds.listRelatives(lc, s=True)[0]
    for axis in "xyz":
        cmds.setAttr("%s.lp%s"%(lc, axis), l=False, ch=True, k=True)
        cmds.setAttr("%s.ls%s"%(lc, axis), l=False, ch=True, k=True)
        cmds.setAttr("%s.lp%s"%(lc, axis), l=True, ch=False, k=False)
        cmds.setAttr("%s.ls%s"%(lc, axis), l=True, ch=False, k=False)
    cmds.setAttr("%s.visibility"%(lc), 0)
    return lc

def SwitchLocator(sel):
    for s in sel:
        attr_list = cmds.listAttr(s, userDefined=True)
        if not attr_list:
            continue
        attr_list.remove("joint")
        attr_list.remove("Ctrl")
        if not attr_list:
            continue
        lc = CreateLocator(name="LC_%s"%(s.replace("_Grp", "")))
        for attr in attr_list:
            cmds.addAttr(lc, ln=attr, at="long", min=0, max=1, dv=0, k=True)
            cmds.connectAttr("%s.%s"%(lc, attr), "%s.%s"%(s, attr))

def VisibilityLocator(sel):
    lc = CreateLocator(name="LC_Visibility")
    for s in sel:
        if "Root" in s:
            continue
        cmds.addAttr(lc, ln=s.replace("_Grp", ""), at="long", min=0, max=1, dv=1, k=True)
        cmds.connectAttr("%s.%s"%(lc, s.replace("_Grp", "")), "%s.visibility"%(s))

def RigLocator():
    sel = cmds.ls(sl=True)
    SwitchLocator(sel)
    VisibilityLocator(sel)

def DistributeShape():
    sel = cmds.ls(sl=True)
    shape = cmds.listRelatives(sel[0], s=True)[0]
    sel = sel[1:]

    for s in sel:
        tf = [s]
        if cmds.attributeQuery("Ctrl", node=s, exists=True):
            tf = cmds.listConnections("%s.Ctrl"%(s), s=True, d=False)
        for t in tf:
            ins = cmds.instance(shape)[0]
            ins_shape = cmds.listRelatives(ins, s=True)[0]
            cmds.parent("%s|%s"%(ins, ins_shape), t, s=True, r=True)
            cmds.delete(ins)

def ShapeDelete():
    sel = cmds.ls(sl=True)
    
    for s in sel:
        tf = [s]
        if cmds.attributeQuery("Ctrl", node=s, exists=True):
            tf = cmds.listConnections("%s.Ctrl"%(s), s=True, d=False)
        for t in tf:
            lc = cmds.listRelatives(t, s=True, typ="locator") or []
            if not lc:
                continue
            lc = "%s|%s"%(t, lc[0])
            tmp_tf = cmds.createNode("transform")
            cmds.parent(lc, tmp_tf, s=True, r=True)
            cmds.delete(tmp_tf)