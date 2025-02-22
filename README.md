# README
YSRig  
各部位ごとに自動でリグを作成し、組み立てる事で迅速かつ柔軟にリグを作れるモジュラーリギングシステムです。  
Maya2024で動作確認。  
2025以降は対応していません。

## セットアップ手順
ysrig-publicをダウンロード。  

YSRigフォルダ と userSetup.mel を ドキュメント/maya/2024/scripts 直下へ移動。  

YSRigControlShape.json と YSRigSettings.json を ドキュメント/maya/2024/prefs 直下へ移動。  

<img src="https://github.com/user-attachments/assets/1122e760-61eb-4930-a574-4851da06171e" width="200">  

Mayaウィンドウ上部にYSRigメニューが追加されます。

## 対応するモデルの条件
* ジョイントに "JT_" "JNT_" "_joint" のように、jointに特定の統一された命名がされている。
* 同一名ジョイントが存在しない。
* ジョイントの主軸がX軸である。(ジョイントのX軸が子どものジョイント、もしくはその逆を向いている。)
* IKが入る肘や膝のjointOrientアトリビュートが一軸(曲がる軸)以外0である。
* IKが入る肘や膝の優先角が設定されていること。
* Rootジョイント(ワールド原点にあるジョイント階層の一番親)がある。  
  Rootジョイントが無い場合は、ワールド原点にジョイントを作成し、ジョイント階層を丸ごとその子どもにしてください。
* RootジョイントのjointOrientアトリビュートが0である。

**Mixamoのフリーモデルは特例で対応済み。**

## 使い方
00. **基本的な使い方**
01. **Setup Mixamo Character** (*Mixamoのモデルにリグを作る下準備*)
02. **Create Controller Shape** (*コントローラーのみを作成*)
03. **Root** (*リグ*)
04. **Simple FK** (*リグ*)
05. **Spine** (*リグ*)
06. **Neck FK** (*リグ*)
07. **Arm IKFK** (*リグ*)
08. **Leg IKFK** (*リグ*)
09. **Finger FK** (*リグ*)
10. **Remove Rig**　(*リグの削除*)
11. **Edit Look** (*コントローラーの色、太さ変更*)
12. **Create Locator** (*IKFKやワールドローカル等制御用のロケーターを作成*)
13. **Distribute Locator**　(*制御用ロケーターをコントローラーと接続*)
14. **Remove Locator**  (*制御用ロケーターを削除*)
15. **Hide Utility Node**  (*チャンネルボックス整理*)

### 0. 基本的な使い方

<img src="https://github.com/user-attachments/assets/2356eeed-587f-420e-861d-ff5125e9cd48" width="400">  

人形のリグの場合、画像のように骨構造を分割してリグを作成していきます。  

**実際にリグを作る際は必ず一番最初にRoot(赤)のリグを作成してください。**  

<img src="https://github.com/user-attachments/assets/c5dab9d5-5e12-4478-96f2-8a1150fe15fd" width="400">  

これは実際にリグを作成する際に使用するウィンドウです。  

このウィンドウではシンプルなFKリグを作成する事ができます。  

このようなウィンドウが7種類あり、それぞれ異なる機能を持っています。  

<img src="https://github.com/user-attachments/assets/c09e6e19-2fcd-4ed7-a3f5-a1193183414b" width="400">  

必要な情報を入力し実行することで、リグが作成されます。
画像は**Neck FK**で作成したリグです。  

<img src="https://github.com/user-attachments/assets/01742ace-b473-4e6b-80ca-e34398814d5b" width="400">  

大きさはある程度自動でフィットするようになっており、事前に変更することも可能ですが、リグを作ってから大きさを変えたい場合は  
画像のように、**ControllVertex**モード(F9) で編集してください。
