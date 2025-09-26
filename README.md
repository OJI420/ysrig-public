# YSRig

**本プラグインは、リグを部位 (モジュール) ごとに分割し、自動でスケルトンとコントローラーを構築する モジュラーリギングシステム です。**  

## システム要件
- OS：Windows10/11
- Maya：2024, 2025, 2026

---

## インストール手順
![Image](https://github.com/user-attachments/assets/04ddd46a-4747-495d-b123-69c31917af4b)
### インストーラーで自動インストール
1. Releaseからzipファイルをダウンロードし解凍
2. setup.batを実行
3. 指示に従いインストール
4. Maya上部メニューにYSRigのメニューが追加されます

### 手動でインストール
1. Releaseからzipがファイルをダウンロードし解凍
2. MAYA_MODULE_PATHが通ったディレクトリにmodulesフォルダの中身をコピー
  - Mayaのデフォルトでは **"ドキュメント\maya\modules"**
  - **"ドキュメント\maya"** にmodulesフォルダが無い場合、ダウンロードしたmodulesフォルダごとコピー
3. Mayaを起動
4. **Windiows -> Settings/Preferences -> Plug-in Manager** から **"ysrig_plugin.py"** の **Loaded** と **Auto load** を有効化
5. Maya上部メニューにYSRigのメニューが追加されます

---
**ツールに関する細かいヘルプは、YSRigメニュー -> Help から確認できます。**  
**不明な点や、不具合等ございましたら、 23au0117@jec.ac.jp までご連絡ください。**
