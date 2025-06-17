# micropythonの関数

micropythonの日本語版リファレンスは以下のサイトから閲覧できます。  
公式リファレンスを読みながらプログラミングできるようになると開発の自由度が大きく広がるので、普段から参照することを意識しましょう。  
[micropythonリファレンス(日本語)](https://micropython-docs-ja.readthedocs.io/ja/latest/library/index.html)

## 固有ライブラリ

### **machine**

micropythonを使って電子工作をするときに必要となるのがこのライブラリです。

#### *Pin*

*Pin*クラスはGPIOの制御に用いられるので頻繁に使います。  

例えば、以下のようにして13番ピンのHIGH, LOWを制御することができます。

```py
#GPIOを制御するためのライブラリをimport
from machine import Pin
#時間を制御するためのライブラリをimport
import time

#13番ピンを出力(OUT)に設定
gate = Pin(13, Pin.OUT)

#インデント内のコードを3回実行
for i in range(3):
    gate.value(0)#gate出力を0に
    time.sleep(3)#3秒待機
    gate.value(1)#gate出力を1に
    time.sleep(3)#3秒待機

#最後に出力を0にしておくことを忘れない
gate.value(0)
print("finish")
```