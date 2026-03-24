# bme280_simple.py
from machine import I2C
import struct
import time

class BME280Simple:
    def __init__(self, i2c, addr=0x76):
        self.i2c = i2c
        self.addr = addr
        # リセット
        self._write_reg(0xE0, b'\xB6')
        time.sleep_ms(300)
        # キャリブレーションデータ読み込み
        calib = self.i2c.readfrom_mem(self.addr, 0x88, 26)
        calib_h = self.i2c.readfrom_mem(self.addr, 0xE1, 7)
        # 温度・圧力用キャリブレーション
        self.dig_T1, self.dig_T2, self.dig_T3, \
        self.dig_P1, self.dig_P2, self.dig_P3, self.dig_P4, self.dig_P5, \
        self.dig_P6, self.dig_P7, self.dig_P8, self.dig_P9 = struct.unpack('<HhhHhhhhhhhh', calib)
        # 湿度用キャリブレーション
        self.dig_H1 = self.i2c.readfrom_mem(self.addr, 0xA1, 1)[0]
        self.dig_H2, self.dig_H3, e4, e5, e6 = struct.unpack('<hBbBb', calib_h)
        self.dig_H2 = self.dig_H2
        self.dig_H3 = self.dig_H3
        self.dig_H4 = (e4 << 4) | (e5 & 0x0F)
        self.dig_H5 = (e6 << 4) | (e5 >> 4)
        self.dig_H6 = struct.unpack('b', calib_h[6:7])[0]
        # 動作モード・フィルタ・オーバーサンプリング設定
        # ctrl_hum → ctrl_meas → config の順で設定すること
        # 湿度 1x, 温度 1x, 圧力 1x, 正常モード
        self._write_reg(0xF2, b'\x01')  # ctrl_hum
        self._write_reg(0xF4, b'\x27')  # ctrl_meas
        self._write_reg(0xF5, b'\xA0')  # config

    def _write_reg(self, reg, data):
        self.i2c.writeto_mem(self.addr, reg, data)

    def read_raw(self):
        # レジスタ 0xF7 から 8 バイト（圧力3、温度3、湿度2）を一括読み
        data = self.i2c.readfrom_mem(self.addr, 0xF7, 8)
        pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
        hum_raw  = (data[6] << 8)  | data[7]
        return temp_raw, pres_raw, hum_raw

    def compensate(self, temp_raw, pres_raw, hum_raw):
        # 温度補正
        var1 = (((temp_raw / 16384) - (self.dig_T1 / 1024)) * self.dig_T2)
        var2 = (((temp_raw / 131072) - (self.dig_T1 / 8192))**2) * self.dig_T3
        t_fine = var1 + var2
        temperature = t_fine / 5120.0

        # 圧力補正
        var1 = (t_fine / 2) - 64000
        var2 = var1 * var1 * (self.dig_P6) / 32768
        var2 = var2 + var1 * (self.dig_P5) * 2
        var2 = (var2 / 4) + (self.dig_P4 * 65536)
        var1 = (self.dig_P3 * var1 * var1 / 524288 + self.dig_P2 * var1) / 524288
        var1 = (1 + var1 / 32768) * self.dig_P1
        pressure = 1048576 - pres_raw
        pressure = (pressure - var2 / 4096) * 6250 / var1
        var1 = self.dig_P9 * pressure * pressure / 2147483648
        var2 = pressure * self.dig_P8 / 32768
        pressure = pressure + (var1 + var2 + self.dig_P7) / 16.0

        # 湿度補正
        h = t_fine - 76800
        h = (hum_raw - (self.dig_H4 * 64 + self.dig_H5 / 16384 * h)) * \
            (self.dig_H2 / 65536 * (1 + self.dig_H6 / 67108864 * h * (1 + self.dig_H3 / 67108864 * h)))
        humidity = h * (1 - self.dig_H1 * h / 524288)
        if humidity > 100:
            humidity = 100
        elif humidity < 0:
            humidity = 0

        return temperature, pressure/100, humidity

    def read_compensated(self):
        tr, pr, hr = self.read_raw()
        return self.compensate(tr, pr, hr)
