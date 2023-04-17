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