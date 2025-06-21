from ctypes import addressof
import smbus


# オブジェクト生成
i2c = smbus.SMBus(1)  # sudo i2cdetect  1で見つかったので

# 定義
# アドレス等
# スレーブアドレスの下位ビット選択
SA0_LOW_ADDRESS = 0x5C  # SA0(4ピン)をGNDに接続する (01011100x)
SA0_HIGH_ADDRESS = 0x5D  # SA0(4ピン)をVDDに接続する　(01011101x)
address = SA0_HIGH_ADDRESS

TEST_REG_NACK = -1

LPS25H_WHO_ID = 0xBD  # (10111101)

# デバイスタイプ
device_25H = 0
device_auto = 1
device = device_25H

# sa0の状態
sa0_low = 0
sa0_high = 1
sa0_auto = 2

REF_P_XL = 0x08
REF_P_L = 0x09
REF_P_H = 0x0A

WHO_AM_I = 0x0F

RES_CONF = 0x10

CTRL_REG1 = 0x20
CTRL_REG2 = 0x21
CTRL_REG3 = 0x22
CTRL_REG4 = 0x23

STATUS_REG = 0x27

PRESS_OUT_XL = 0x28
PRESS_OUT_L = 0x29
PRESS_OUT_H = 0x2A

TEMP_OUT_L = 0x2B
TEMP_OUT_H = 0x2C

FIFO_CTRL = 0x2E
FIFO_STATUS = 0x2F

RPDS_L = 0x39
RPDS_H = 0x3A

INTERRUPT_CFG = -1
INT_SOURCE = -2
THS_P_L = -3
THS_P_H = -4

LPS25H_INTERRUPT_CFG = 0x24
LPS25H_INT_SOURCE = 0x25
LPS25H_THS_P_L = 0x30
LPS25H_THS_P_H = 0x31

translated_regs = [0]

# 関数一覧

# LPS25HBのステータスを取得する


def testWhoAmI():
    return i2c.read_i2c_block_data(address, WHO_AM_I, 1)

# 接続されているデバイスがLPS25HBか確認する


def detectDevice():
    id = testWhoAmI()
    if (id[0] == LPS25H_WHO_ID):
        return True

    return False

# LPS25HBが接続されているとき初期化する


def LPS_init():

    if (detectDevice() == False):
        return False

    else:
        translated_regs.append(LPS25H_INTERRUPT_CFG)
        translated_regs.append(LPS25H_INT_SOURCE)
        translated_regs.append(LPS25H_THS_P_L)
        translated_regs.append(LPS25H_THS_P_H)
        return True

# コマンドを送ってデータを送る(1バイト)


def writeReg(reg, value):
    if(reg < 0):
        reg = translated_regs[-reg]
    val = [value]
    i2c.write_i2c_block_data(address, reg, val)

#　コマンドを送ってデータを受け取る(1バイト)
# def writeReg(reg):
  #  if(reg < 0):
   #     reg = translated_regs[-reg]
    #value = i2c.write_i2c_block_data(address,reg,1)
    # return value

# LPS25HBの読み込みモードや読み込み周期を変更する


def enableDefault():
    if (device == device_25H):
        # 0xB0 = 0b10110000
        # PD = 1 (active mode);  ODR = 011 (12.5 Hzで気圧と気温を出力する)
        writeReg(CTRL_REG1, 0xB0)

# 大気圧を取得する(3バイト)


def readPressureRaw():
    p = i2c.read_i2c_block_data(address, PRESS_OUT_XL, 1)
    p = p + i2c.read_i2c_block_data(address, PRESS_OUT_L, 1)
    p = p + i2c.read_i2c_block_data(address, PRESS_OUT_H, 1)

    # 受け取ったそれぞれのデータを変換して一つのデータにする
    return p[2] << 16 | p[1] << 8 | p[0]

# 大気圧をhPaで返す　計算((mbar)/(hPa))


def readPressureMillibars():
    return readPressureRaw() / 4096

# 大気圧をinHgで返す


def readPressureInchesHg():
    return readPressureRaw() / 138706.5
# 気温を取得する(2バイト)


def readTemperatureRaw():
    t = i2c.read_i2c_block_data(address, TEMP_OUT_L, 1)
    t = t + i2c.read_i2c_block_data(address, TEMP_OUT_H, 1)
    # 受け取ったそれぞれのデータを変換して一つのデータにする
    return (t[1] << 8 | t[0]) - 65535
# 気温を摂氏で返す


def readTemperatureC():
    return 42.5 + readTemperatureRaw() / 480
# 気温を華氏で返す


def readTemperatureF():
    return 108.5 + readTemperatureRaw() / 480 * 1.8
# 気圧から標高(m)を推定計算して返す


def pressureToAltitudeMeters(pressure_mbar, altimeter_setting_mbar=1013.25):
    return (1 - pow(pressure_mbar / altimeter_setting_mbar, 0.190263)) * 44330.8
# 気圧から標高(feet)を推定計算して返す


def pressureToAltitudeFeet(pressure_inHg, altimeter_setting_inHg=29.9213):
    return (1 - pow(pressure_inHg / altimeter_setting_inHg, 0.190263)) * 145442
