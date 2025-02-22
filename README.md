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
00. 基本的な使い方  
01. Setup Mixamo Character  
02. Create Controller Shape  
03. Root  
04. Simple FK  
05. Spine  
06. Neck FK  
07. Arm IKFK  
08. Leg IKFK  
09. Finger FK  
10. Remove Rig  
11. Edit Look
12. Create Locator
13. Distribute Locator
14. Remove Locator
15. Hide Utility Node

### 0. 基本的な使い方

<img src="https://github.com/user-attachments/assets/2356eeed-587f-420e-861d-ff5125e9cd48" width="400">  

人形のリグの場合、画像のように骨構造を分割してリグを作成していきます。

