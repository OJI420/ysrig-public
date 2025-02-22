import itertools
import maya.cmds as cmds
import importlib
import YSRig.YSRig as YSRig
importlib.reload(YSRig)

def PathSprit(input_string):
    result_list = input_string.split('|')
    
    result_list = [item for item in result_list if item]
    
    return result_list
    
def ConnectMatrix(src, dest, type="World", tl=False, rt=False, sc=False, sh=False, o=True):
    """ Set Offset """
    tmp_offset = cmds.createNode("multMatrix", name="tmp_Mm")

    cmds.connectAttr("%s.worldMatrix[0]"%(dest), "%s.matrixIn[0]"%(tmp_offset))
    cmds.connectAttr("%s.worldInverseMatrix[0]"%(src), "%s.matrixIn[1]"%(tmp_offset))

    offseMatrix = cmds.getAttr("%s.matrixSum"%(tmp_offset))
    mm = cmds.createNode("multMatrix", name="Mm_%s"%(dest))

    cmds.setAttr("%s.matrixIn[0]"%(mm), offseMatrix, type="matrix")
    cmds.delete(tmp_offset)

    # Local 
    if type == "Local":
        parents1 = cmds.listRelatives(src, allParents=True, fullPath=True)[0] + "|" + src
        parents2 = cmds.listRelatives(dest, allParents=True, fullPath=True)[0]
        
        parent_list1 = list(reversed(PathSprit(parents1)))
        parent_list2 = list(reversed(PathSprit(parents2)))
        
        root_node = ""
        
        for list1, list2 in itertools.product(parent_list1, parent_list2):
            if list1 in list2:
                root_node = list1
                break
                
        src_parent_nodes = []
        for list1 in parent_list1:
            if list1 in root_node:
                break
            else:
                src_parent_nodes.append(list1)
        tmp_parent_nodes = []
        for list2 in parent_list2:
            if list2 in root_node:
                break
            else:
                tmp_parent_nodes.append(list2)
                
        dest_parent_nodes = list(reversed(tmp_parent_nodes))
        #multMatrix connect
        for i,srcs in enumerate(src_parent_nodes, start=1):
            cmds.connectAttr("%s.matrix"%(srcs),"%s.matrixIn[%s]"%(mm,i))
            
        src_len = len(src_parent_nodes)
        
        for i,dests in enumerate(dest_parent_nodes, start=src_len + 1):
            cmds.connectAttr("%s.inverseMatrix"%(dests),"%s.matrixIn[%s]"%(mm,i))
            
        all_len = src_len + len(dest_parent_nodes) + 1
    
    # World
    elif type == "World":
        cmds.connectAttr("%s.worldMatrix[0]"%(src),"%s.matrixIn[1]"%(mm))
        cmds.connectAttr("%s.parentInverseMatrix[0]"%(dest),"%s.matrixIn[2]"%(mm))
        
        all_len = 3
    if o:
        if cmds.nodeType(dest) == "joint":
            #orient
            tmp_cm = cmds.createNode("composeMatrix", name="tmp_Cm")
            tmp_im = cmds.createNode("inverseMatrix", name="tmp_Im")
            cmds.connectAttr("%s.jointOrient"%(dest), "%s.inputRotate"%(tmp_cm))
            cmds.connectAttr("%s.outputMatrix"%(tmp_cm),"%s.inputMatrix"%(tmp_im))
            cmds.setAttr("%s.matrixIn[%s]"%(mm,all_len),cmds.getAttr("%s.outputMatrix"%(tmp_im)), type="matrix")
            cmds.delete(tmp_cm)
    
    dm = cmds.createNode("decomposeMatrix", name="Dm_%s"%(dest))
    cmds.connectAttr("%s.matrixSum"%(mm),"%s.inputMatrix"%(dm))
    
    #connect Transform
    if tl == True:
        for axis in "XYZ":
            cmds.connectAttr("%s.outputTranslate%s"%(dm,axis),"%s.translate%s"%(dest,axis))
    if rt == True:
        for axis in "XYZ":
            cmds.connectAttr("%s.outputRotate%s"%(dm,axis),"%s.rotate%s"%(dest,axis))
    if sc == True:
        for axis in "XYZ":
            cmds.connectAttr("%s.outputScale%s"%(dm,axis),"%s.scale%s"%(dest,axis))
    if sh == True:
        cmds.connectAttr("%s.outputShear"%(dm),"%s.shear"%(dest))
        
    return mm, dm

def AllConnectAttr(src, dest):
    for axis in "XYZ":
        cmds.connectAttr("%s.translate%s"%(src, axis), "%s.translate%s"%(dest, axis))
        cmds.connectAttr("%s.rotate%s"%(src, axis), "%s.rotate%s"%(dest, axis))
        cmds.connectAttr("%s.scale%s"%(src, axis), "%s.scale%s"%(dest, axis))
    cmds.connectAttr("%s.shearXY"%(src), "%s.shearXY"%(dest))
    cmds.connectAttr("%s.shearXZ"%(src), "%s.shearXZ"%(dest))
    cmds.connectAttr("%s.shearYZ"%(src), "%s.shearYZ"%(dest))

def ConnectWeightWorldMatrix(list, group, MatrixAnchor, floatMath=False, pairBlend=False):
    dv = round(1/len(list), 3)
    step = dv
    fm_list = []
    pb_list = []
    cmds.addAttr(group, ln="WL", at="long", min=0, max=1, dv=1, k=True)
    for node in list:
        dm = ConnectMatrix(MatrixAnchor, node, type="World", rt=True)[1]
        fm = cmds.createNode("floatMath", name="Fm_%s"%(node))
        pb = cmds.createNode("pairBlend", name="Pb_%s"%(node))
        cmds.addAttr(node, ln="weight", at="double", min=0, max=1, dv=dv, k=True)
        cmds.setAttr("%s.operation"%(fm), 2)
        cmds.setAttr("%s.rotInterpolation"%(pb), 1)
        cmds.connectAttr("%s.WL"%(group), "%s.floatA"%(fm))
        cmds.connectAttr("%s.weight"%(node), "%s.floatB"%(fm))
        cmds.connectAttr("%s.outFloat"%(fm), "%s.weight"%(pb))
        cmds.connectAttr("%s.outputRotate"%(dm), "%s.inRotate2"%(pb))
        for axis in "XYZ":
            cmds.connectAttr("%s.outRotate%s"%(pb, axis), "%s.rotate%s"%(node, axis), f=True)
        fm_list.append(fm)
        pb_list.append(pb)
        dv += step
        if node == list[-2]:
            dv = 1
    if floatMath and pairBlend:
        return fm_list, pb_list
    elif floatMath:
        return fm_list
    elif pairBlend:
        return pb_list
    else:
        return
    
def ConnectPairBlend(src1, src2, dest):
    pb = cmds.createNode("pairBlend", name="Pb_%s"%(dest))
    cmds.setAttr("%s.rotInterpolation"%(pb), 1)
    cmds.connectAttr("%s.rotate"%(src1), "%s.inRotate1"%(pb))
    cmds.connectAttr("%s.rotate"%(src2), "%s.inRotate2"%(pb))
    for axis in "XYZ":
        cmds.connectAttr("%s.outRotate%s"%(pb, axis), "%s.rotate%s"%(dest, axis))
    return pb

def ConnectWeight(node, attr, type, pb_list):
    if not cmds.attributeQuery(attr, node=node, exists=True):
        cmds.addAttr(node, ln=attr, at=type, min=0, max=1, dv=1, k=True)
    if isinstance(pb_list, str):
        pb_list = [pb_list]
    for pb in pb_list:
        cmds.connectAttr("%s.%s"%(node, attr), "%s.weight"%(pb))

def connectVisibility(attr, tr, fl):
    if tr:
        if isinstance(tr, str):
            tr = [tr]
        for t in tr:
            cmds.connectAttr(attr, "%s.visibility"%(t))
    if fl:
        if isinstance(fl, str):
            fl = [fl]
        for f in fl:
            rv = cmds.createNode("reverse", name="Rv_%s"%(f))
            cmds.connectAttr(attr, "%s.inputX"%(rv))
            cmds.connectAttr("%s.outputX"%(rv), "%s.visibility"%(f))

def ConnectWorldMatrix(node, attr, group, MatrixAnchor, tl=True, rt=True, inv=False):
    cmds.addAttr(group, ln=attr, at="long", min=0, max=1, dv=1, k=True)
    if tl and rt:
        pc = cmds.parentConstraint(MatrixAnchor, node, mo=True, name="Pc_%s"%(node))[0]
    if tl and not rt:
        pc = cmds.pointConstraint(MatrixAnchor, node, mo=True, name="Poc_%s"%(node))[0]
    if not tl and rt:
        pc = cmds.orientConstraint(MatrixAnchor, node, mo=True, name="Oc_%s"%(node))[0]
    pb = cmds.createNode("pairBlend", name="Pb_%s"%(node))
    cmds.setAttr("%s.rotInterpolation"%(pb), 1)
    i = 2
    if inv:
        i -= 1
    if tl:
        cmds.connectAttr("%s.constraintTranslate"%(pc), "%s.inTranslate%s"%(pb, i))
    if rt:
        cmds.connectAttr("%s.constraintRotate"%(pc), "%s.inRotate%s"%(pb, i))
    cmds.connectAttr("%s.%s"%(group, attr), "%s.weight"%(pb))
    for axis in "XYZ":
        if tl:
            cmds.connectAttr("%s.outTranslate%s"%(pb, axis), "%s.translate%s"%(node, axis), f=True)
        if rt:
            cmds.connectAttr("%s.outRotate%s"%(pb, axis), "%s.rotate%s"%(node, axis), f=True)
    return pb

def ConnectRotatePivot(src, dest):
    cm = cmds.createNode("colorMath", name="Cm_%s"%(dest))
    cmds.connectAttr("%s.translate"%(src), "%s.colorA"%(cm))
    cmds.connectAttr("%s.rotatePivot"%(src), "%s.colorB"%(cm))
    cmds.connectAttr("%s.outColorR"%(cm), "%s.translateX"%(dest))
    cmds.connectAttr("%s.outColorG"%(cm), "%s.translateY"%(dest))
    cmds.connectAttr("%s.outColorB"%(cm), "%s.translateZ"%(dest))
    return cm

def ConnectJointMatrix(src, dest, type="World", connect=True):
    mmr, dmr = ConnectMatrix(src, dest, type=type, tl=False, rt=connect, sc=False, sh=False, o=True)
    mmr = cmds.rename(mmr, mmr.replace("Mm_", "Mm_Rot_"))
    dmr = cmds.rename(dmr, dmr.replace("Dm_", "Dm_Rot_"))

    mmp, dmp = ConnectMatrix(src, dest, type=type, tl=connect, rt=False, sc=False, sh=False, o=False)
    mmp = cmds.rename(mmp, mmp.replace("Mm_", "Mm_Pos_"))
    dmp = cmds.rename(dmp, dmp.replace("Dm_", "Dm_Pos_"))

    return  mmr, dmr, mmp, dmp

def ConnectInfo(grp, attr, node_list):
    cmds.addAttr(grp, ln=attr, dt="string", multi=True)
    for i, node in enumerate(node_list):
        cmds.connectAttr("%s.message"%(node), "%s.%s[%d]"%(grp, attr, i))