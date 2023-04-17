# ハードウェア開発ことはじめ

## 資料の目的

本資料はFUSiONの新人メンバーに対して効率よくモノづくりの電子工作(Hardware)分野の基礎を習得してももらうことを目的として作られている。この新人教育用資料での到達目標は以下のように設定する。

* 過去のFUSiONの引継ぎ資料を読んで理解できる
* センサから生データをとってきて任意の式に代入できる
* 簡単なアクチュエーターを制御できる

## 資料の構成

本教育資料は安価かつ汎用性が高い秋月電子製のマイコンボード「[AE-RP2040](https://akizukidenshi.com/catalog/g/gK-17542/)」を用いる。
![AE-RP2040](https://akizukidenshi.com/img/goods/C/K-17542.jpg)

### AE-2040のここがすごい

* 書込み口がType-C
* RaspberryPi picoに搭載され名を馳せた「RP2040」チップを使用
* 小型で安価
* micro-python, C/C++に対応

本資料は読者として、ほとんど電子工作をしたことがない人もしくはやったことはあるが知識を整理したい人を想定する。

0. Lチカしてみよう(宿題)
    ・実行環境は[Thonny]  
    ・プログラム言語は[micropython]  
    上の制約の中でLチカ(LED点滅制御)を初回研修日までに完了してください。
1. トランジスタの仕組みとモーターの動作  
    MOSFETを用いてモーターを駆動させる。  
2. センサの信号(I2C, UART)  
    プルアップ抵抗・プルダウン抵抗への理解
    I2CやUARTの通信規格を知る。
3. センサを使ってみよう  
    実際にマイコンボードを使ってセンサの値を取得してみる。
    データシートを読めるようになる。
4. 回路設計をしてみよう  
    1~3の機能を持つ基板を設計してみる。  
    部品紹介  
    電源計算

## 用意するもの
この講座では上の4章構成で電気回路の設計について学ぶ。  
それぞれの講座を通して必要になる部品は以下の通りです。
||初使用回|部品名|販売リンク|
|----|-----|----|----|
|![](https://m.media-amazon.com/images/I/51Olo38hQtL._AC_SX679_.jpg)|0|はんだこて|https://www.amazon.co.jp/%E7%99%BD%E5%85%89-HAKKO-FX600-02-%E3%83%80%E3%82%A4%E3%83%A4%E3%83%AB%E5%BC%8F%E6%B8%A9%E5%BA%A6%E5%88%B6%E5%BE%A1%E3%81%AF%E3%82%93%E3%81%A0%E3%81%93%E3%81%A6-FX600/dp/B006MQD7M4/ref=sr_1_1?crid=2ESSF447QFZTB&keywords=hakko+%E3%81%AF%E3%82%93%E3%81%A0%E3%81%93%E3%81%A6+fx600-02&qid=1681710452&sprefix=hakko+%E3%81%AF%E3%82%93%E3%81%A0%E3%81%93%E3%81%A6%2Caps%2C381&sr=8-1|
|![](https://akizukidenshi.com/img/goods/C/P-05294.jpg)|0|ブレッドボード|https://akizukidenshi.com/catalog/g/gP-05294/|
|![](https://akizukidenshi.com/img/goods/2/C-15869.jpg)|0|ジャンパワイヤ|https://akizukidenshi.com/catalog/g/gC-15869/|
|![](https://akizukidenshi.com/img/goods/C/I-12687.jpg)|0|LED(赤)|https://akizukidenshi.com/catalog/g/gI-12687/|
|![](https://akizukidenshi.com/img/goods/C/R-25332.jpg)|0|抵抗(3.3kΩ)|https://akizukidenshi.com/catalog/g/gR-25332/|
|![](https://akizukidenshi.com/img/goods/C/K-17542.jpg)|0|マイコン|https://akizukidenshi.com/catalog/g/gK-17542/|
|![](https://akizukidenshi.com/img/goods/4/I-02414.JPG)|1|MOSFET|https://akizukidenshi.com/catalog/g/gI-02414/|
|![]|1|モーター|https://akizukidenshi.com/catalog/g/gP-09169/|
|![](https://akizukidenshi.com/img/goods/C/I-02228.jpg)|1|整流ダイオード|https://akizukidenshi.com/catalog/g/gI-02228/|
|![](https://akizukidenshi.com/img/goods/C/K-09421.jpg)|3|温湿度気圧センサ|https://akizukidenshi.com/catalog/g/gK-09421/|