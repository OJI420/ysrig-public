# YSRigのプラグインロード用のスクリプトです。
# Mayaのビューポート上にドラッグアンドドロップしてください

from maya import cmds

def onMayaDroppedPythonFile(*args, **kwargs):
    cmds.loadPlugin("ysrig_plugin.py")
    cmds.pluginInfo("ysrig_plugin.py", edit=True, autoload=True)