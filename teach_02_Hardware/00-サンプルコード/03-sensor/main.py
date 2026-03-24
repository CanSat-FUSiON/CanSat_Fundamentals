# main.py
from machine import I2C, Pin
from bme280_simple import BME280Simple
import time

# I2C0, SDA=GP0, SCL=GP1, 100kHz
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)
bme = BME280Simple(i2c)

while True:
    temp, pres, hum = bme.read_compensated()
    print("Temp: {:.2f} C, Pres: {:.2f} hPa, Hum: {:.2f} %".format(temp, pres, hum))
    time.sleep(2)
