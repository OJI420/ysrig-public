import sys
import shutil
import os
import json
from PySide6 import QtWidgets, QtCore, QtGui


# --- 定数とパス設定 ---
# MayaのドキュメントパスをOS標準の方法で取得
# 注: Mayaが標準以外の場所にドキュメントフォルダを作成している場合は手動での指定が必要です
MAYA_DOC_PATH = os.path.join(os.path.expanduser("~"), "Documents", "maya")
MAYA_MOD_PATH = os.path.join(MAYA_DOC_PATH, "modules")

# スクリプト自身のパス
CURRENT_DIR = os.path.dirname(__file__)

VERSION = "2.1.3"
TITLE = f"- YSRig v{VERSION} - Setup"

WINDOW_COLOR = "80, 90, 85"
WINDOW_COLOR_2 = "60, 90, 110"
WINDOW_COLOR_3 = "255, 255, 255"
BACK_COLOR_1 = "60, 70, 65"
BACK_COLOR_2 = "180, 180, 180"
BUTTON_COLOR_1 = "40, 50, 45"
BUTTON_COLOR_2 = "30, 60, 80"
BUTTON_COLOR_3 = "200, 200, 200"
STR_COLOR_1 = "230, 215, 215"
STR_COLOR_2 = "170, 170, 175"
STR_COLOR_3 = "10, 0, 0"
ERROR_COLOR = "255, 0, 0"


class Gui(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.window()
        self.gui()
        self.set_settings()

    def window(self):
        self.setWindowTitle(TITLE)
        self.setObjectName(TITLE)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setMinimumWidth(700)
        self.setStyleSheet(f"background-color: rgb({WINDOW_COLOR});")

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

    def gui(self):
        label = QtWidgets.QLabel(f"YSRig ver {VERSION}")
        label.setStyleSheet(f"color: rgb({STR_COLOR_1});")
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        label.setFont(font)
        label.setAlignment(QtCore.Qt.AlignCenter)

        self.path_edit = YSPathEdit(label="インストールパス")

        install_button = YSPushButton(label="インストール")
        install_button.clicked.connect(self.install)

        self.main_layout.addWidget(label)
        self.main_layout.addWidget(self.path_edit)
        self.main_layout.addWidget(install_button)

    def set_settings(self):
        # デフォルトのインストールパスとして推定したパスを設定
        self.path_edit.set(MAYA_MOD_PATH)

    def install(self):
        install_path = self.path_edit.get()

        # --- ここからが変更箇所 ---
        # パスがデフォルトのmodulesパスかどうかを判定
        is_default_path = (os.path.normpath(install_path) == os.path.normpath(MAYA_MOD_PATH))

        # パスが存在しない場合の処理
        if not os.path.isdir(install_path):
            # もしデフォルトパスなら、フォルダを自動作成する
            if is_default_path:
                try:
                    os.makedirs(install_path)
                    print(f"INFO: modulesフォルダを新規作成しました: {install_path}") # ログ代わりのprint
                except OSError as e:
                    QtWidgets.QMessageBox.critical(
                        self, 
                        "エラー", 
                        f"modulesフォルダの作成に失敗しました。\n書き込み権限を確認してください。\n\n詳細: {e}"
                    )
                    return
            # デフォルトパス以外で、フォルダが存在しない場合はエラー
            else:
                QtWidgets.QMessageBox.critical(self, "エラー", "指定されたインストールパスが存在しません。")
                return
        # --- 変更箇所はここまで ---

        ysrig_install_dir = os.path.join(install_path, "YSRig")
        ysrig_mod_file = os.path.join(install_path, "YSRig.mod")

        # 既にインストールされている場合の処理
        if os.path.isdir(ysrig_install_dir):
            result = YSDialog(self)
            ok, should_migrate_settings = result.get_result()
            if not ok:
                return # キャンセルされた

            # 設定を一時ファイルにエクスポート
            if should_migrate_settings:
                # (一時ファイルの扱いは、以前の提案通りtempfileを使うのが理想です)
                import tempfile
                temp_dir = tempfile.gettempdir()
                tmp_settings_file = os.path.join(temp_dir, "ysrig_tmp_settings.json")
                export(tmp_settings_file, ysrig_install_dir)

            # 古いバージョンを削除
            shutil.rmtree(ysrig_install_dir)
            if os.path.exists(ysrig_mod_file):
                os.remove(ysrig_mod_file)

        # ファイルのコピー
        source_dir = os.path.join("modules", "YSRig")
        source_mod = os.path.join("modules", "YSRig.mod")

        try:
            copy_folder(source_dir, install_path)
            shutil.copy(source_mod, ysrig_mod_file)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "コピーエラー", f"ファイルのコピー中にエラーが発生しました。\n\n詳細: {e}")
            return


        # 設定を引き継ぐ場合はインポート
        if 'should_migrate_settings' in locals() and should_migrate_settings:
            import_(tmp_settings_file, ysrig_install_dir)
            os.remove(tmp_settings_file)

        # --- 完了メッセージ ---
        M = SuccessMessage(self)
        self.close()

# --- 各種UIクラス ---

class YSPushButton(QtWidgets.QPushButton):
    def __init__(self, label):
        super().__init__(label)
        self.setStyleSheet(f"background-color: rgb({BUTTON_COLOR_1}); color: rgb({STR_COLOR_1});")

    def set_text(self, text):
        self.setText(text)


class YSPathEdit(QtWidgets.QWidget):
    def __init__(self, label="", placeholder_text=""):
        super().__init__()
        self.main_layout = QtWidgets.QGridLayout(self)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.sub_layout = QtWidgets.QHBoxLayout()
        self.sub_layout.setSpacing(10)
        self.sub_layout.setContentsMargins(0, 0, 0, 0)
        self.label = QtWidgets.QLabel(f"{label} :")
        self.label.setStyleSheet(f"color: rgb({STR_COLOR_1});")
        self.label.setAlignment(QtCore.Qt.AlignRight)
        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setPlaceholderText(placeholder_text)
        self.line_edit.setStyleSheet(f"background-color: rgb({BACK_COLOR_1}); color: rgb({STR_COLOR_1});")
        self.button = YSPushButton(" . . . ")
        self.button.clicked.connect(self.call)
        self.sub_layout.addWidget(self.line_edit)
        self.sub_layout.addWidget(self.button)
        self.main_layout.addWidget(self.label, 0, 0)
        self.main_layout.addLayout(self.sub_layout, 0, 1, 1, 2)

    def call(self):
        current_path = self.get() or MAYA_MOD_PATH
        result = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "インストール先のフォルダを選択",
            current_path
        )
        if result:
            self.set(result)

    def set(self, data):
        self.line_edit.setText(data)

    def get(self):
        return self.line_edit.text()


class YSCheckBox(QtWidgets.QWidget):
    def __init__(self, label=""):
        super().__init__()
        self.main_layout = QtWidgets.QGridLayout(self)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.label = QtWidgets.QLabel(f"{label} :")
        self.label.setAlignment(QtCore.Qt.AlignRight)
        self.label.setStyleSheet(f"color: rgb({STR_COLOR_1});")

        self.checkbox = QtWidgets.QCheckBox()

        self.main_layout.addWidget(self.label, 0, 0)
        self.main_layout.addWidget(self.checkbox, 0, 1, 1, 2)

    def set(self, data):
        self.checkbox.setChecked(data)

    def get(self):
        return self.checkbox.isChecked()


class YSDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.window()
        self.gui()
        self.result = self.exec()

    def window(self):
        self.setWindowTitle(f"{TITLE} -")
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setStyleSheet(f"background-color: rgb({WINDOW_COLOR_2});")
        self.setMinimumWidth(300)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 20, 10, 10)

    def gui(self):
        self.label = QtWidgets.QLabel("YSrigはすでにインストールされています。")
        self.label.setStyleSheet(f"color: rgb({STR_COLOR_1});")
        self.layout.addWidget(self.label)

        self.check_box = YSCheckBox("設定を引き継いでインストール")
        self.check_box.set(1)
        self.layout.addWidget(self.check_box)

        self.sub_layout = QtWidgets.QGridLayout()

        self.ok_button = QtWidgets.QPushButton("OK")
        self.ok_button.setStyleSheet(f"color: rgb({STR_COLOR_1}); background-color: rgb({BUTTON_COLOR_2});")
        self.ok_button.clicked.connect(self.ok)

        self.cl_button = QtWidgets.QPushButton("Cancel")
        self.cl_button.setStyleSheet(f"color: rgb({STR_COLOR_1}); background-color: rgb({BUTTON_COLOR_2});")
        self.cl_button.clicked.connect(self.cancel)

        self.sub_layout.addWidget(self.ok_button, 1, 0, 1, 2)
        self.sub_layout.addWidget(self.cl_button, 1, 2, 1, 2)

        self.layout.addLayout(self.sub_layout)

    def get_result(self):
        tf = self.check_box.get()
        if self.result == QtWidgets.QDialog.Accepted:
            return True, tf

        else:
            return False, tf

    def ok(self):
        self.accept()

    def cancel(self):
        self.reject()

    def closeEvent(self, event):
        self.deleteLater()
        super().closeEvent(event)

class SuccessMessage(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.window()
        self.gui()
        self.exec()

    def window(self):
        self.setWindowTitle("インストール完了")
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setStyleSheet(f"background-color: rgb({WINDOW_COLOR_2});")
        self.setMinimumWidth(300)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 20, 10, 10)

    def gui(self):
        self.label1 = QtWidgets.QLabel("YSRigのインストールが完了しました。")
        self.label1.setStyleSheet(f"color: rgb({STR_COLOR_1});")
        self.layout.addWidget(self.label1)
        self.label2 = QtWidgets.QLabel("Mayaを起動（または再起動）し、プラグインマネージャから `ysrig_plugin.py` をロードするか、\ndrag_and_drop.pyをビューポート上にドラッグアンドドロップしてください。")
        self.label2.setStyleSheet(f"color: rgb({STR_COLOR_1});")
        self.layout.addWidget(self.label2)
        self.button = QtWidgets.QPushButton("OK")
        self.button.setStyleSheet(f"color: rgb({STR_COLOR_1}); background-color: rgb({BUTTON_COLOR_2});")
        self.button.clicked.connect(self.close)
        self.button.clicked.connect(self.deleteLater)
        self.layout.addWidget(self.button)


# --- ファイル操作関数 ---

def copy_folder(src: str, dst: str):
    dst_path = os.path.join(dst, os.path.basename(src))
    shutil.copytree(src, dst_path)

def get_prefs_dir(ysrig_dir) -> str:
    pref_dir = os.path.abspath(os.path.join(ysrig_dir, "prefs/ysrig/"))
    return pref_dir

def get_settings(dir) -> dict:
    settings = {}
    jsons = os.listdir(dir)
    for j in jsons:
        if j == "default.json":
            continue
        path = os.path.abspath(os.path.join(dir, j))
        with open(path, 'r') as f:
            settings[j.replace(".json", "")] = json.load(f)
    return settings

def export(file_path, ysrig_dir):
    data = {}
    pref_dir = get_prefs_dir(ysrig_dir)
    mod_dir = os.path.abspath(os.path.join(pref_dir, "modules/"))
    modules = [name for name in os.listdir(mod_dir) if os.path.isdir(os.path.join(mod_dir, name))]
    data["YSRigUserSettingsJSON"] = True
    data["YSRigVersion"] = VERSION

    for mod in modules:
        path = os.path.abspath(os.path.join(mod_dir, f"{mod}/settings/"))
        data[mod] = get_settings(path)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def import_(file_path, ysrig_dir):
    with open(file_path, 'r') as f:
        data: dict = json.load(f)

    modules = list(data.keys())

    ysrig = modules[0]
    ver = data[modules[1]]
    modules = modules[2:]

    pref_dir = get_prefs_dir(ysrig_dir)
    mod_dir = os.path.abspath(os.path.join(pref_dir, "modules/"))

    for mod in modules:
        path = os.path.abspath(os.path.join(mod_dir, f"{mod}/settings/"))
        if not os.path.isdir(path):
            continue

        if mod in data:
            for setting in data[mod]:
                json_path = os.path.abspath(os.path.join(path, f"{setting}.json"))
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(data[mod][setting], f, indent=4)

# --- スタンドアロンアプリのエントリーポイント ---
if __name__ == "__main__":
    # QApplicationインスタンスを作成
    app = QtWidgets.QApplication(sys.argv)
    
    # Guiインスタンスを作成して表示
    gui = Gui()
    gui.show()
    
    # アプリケーションのイベントループを開始
    sys.exit(app.exec())