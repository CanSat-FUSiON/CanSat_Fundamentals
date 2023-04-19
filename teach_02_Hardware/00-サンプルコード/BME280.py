#GPIOを制御するライブラリからI2Cに関連するクラスをimport
from machine import I2C,Pin
#センサbme280を使えるようにするライブラリをimport
import bme280

#I2C2を利用するGPIO、通信周波数の指定
i2c=I2C(0,sda=Pin(0),scl=Pin(1),freq=100000)

bme=bme280.BME280(i2c=i2c)

#BME280から値を取得する関数の呼び出し
print(bme.values)