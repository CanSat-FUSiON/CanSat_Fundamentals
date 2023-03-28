# ハードウェア開発ことはじめ


## 資料の目的
本資料はFUSiONの新人メンバーに対して効率よくモノづくりの電子工作(Hardware)分野の基礎を習得してももらうことを目的として作られている。この新人教育用資料での到達目標は以下のように設定する。
* 過去のFUSiONの引継ぎ資料を読んで理解できる
* センサから生データをとってきて任意の式に代入できる
* 簡単なアクチュエーターを制御できる

## 資料の構成
本教育資料は安価かつ汎用性が高い秋月電子製のマイコンボード「[AE-RP2040](https://akizukidenshi.com/catalog/g/gK-17542/)」を用いる。
![AE-RP2040](https://akizukidenshi.com/img/goods/C/K-17542.jpg)

### AE-2040のここがすごい！
* 書込み口がType-C
* RaspberryPi picoに搭載され名を馳せた「RP2040」チップを使用
* 小型で安価
* micro-python, C/C++に対応

本資料は読者として、ほとんど電子工作をしたことがない人もしくはやったことはあるが知識を整理したい人を想定する。

1. トランジスタの仕組みとモーターの動作
    MOSFETを用いてモーターを駆動させる。
2. センサの信号(I2C, UART)
    プルアップ抵抗・プルダウン抵抗への理解
    I2CやUARTの通信規格を知る。
2. センサを使ってみよう
    実際にマイコンボードを使ってセンサの値を取得してみる。
3. 