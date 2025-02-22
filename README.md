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

## 詳細な使い方

