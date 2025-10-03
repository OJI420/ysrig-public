# YSRigのプラグインロード用のスクリプトです。
# Mayaのビューポート上にドラッグアンドドロップしてください

from maya import cmds

plugin_name = "ysrig_plugin.py"

def onMayaDroppedPythonFile(*args, **kwargs):
    cmds.loadPlugin(plugin_name)
    cmds.pluginInfo(plugin_name, edit=True, autoload=True)