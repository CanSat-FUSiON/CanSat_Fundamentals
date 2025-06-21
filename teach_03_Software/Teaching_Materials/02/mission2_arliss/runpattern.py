import RPi.GPIO as GPIO
import time

GPIO.cleanup()

left_front = 8
right_front = 24
left_back = 25
right_back = 23
green_led = 13
nicr_burn = 5


GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(right_front, GPIO.OUT)
GPIO.setup(left_front, GPIO.OUT)
GPIO.setup(right_back, GPIO.OUT)
GPIO.setup(left_back, GPIO.OUT)
GPIO.setup(green_led, GPIO.OUT)
GPIO.setup(nicr_burn, GPIO.OUT)

GPIO.setwarnings(False)


def first():  # 初めにモーターが回りだしてしまうため。(ピン番号変更必須)
    GPIO.output(left_back, GPIO.LOW)


def stop(x=0):
    GPIO.output(right_front, GPIO.LOW)
    GPIO.output(left_front, GPIO.LOW)
    GPIO.output(right_back, GPIO.LOW)
    GPIO.output(right_back, GPIO.LOW)
    if x != 0:
        time.sleep(x)
    return()


def forward(x=0):
    GPIO.output(right_front, GPIO.HIGH)
    GPIO.output(left_front, GPIO.HIGH)
    GPIO.output(right_back, GPIO.LOW)
    GPIO.output(left_back, GPIO.LOW)
    if x != 0:
        time.sleep(x)
    return()


def back(x=0):
    GPIO.output(right_back, GPIO.HIGH)
    GPIO.output(left_back, GPIO.HIGH)
    GPIO.output(right_front, GPIO.LOW)
    GPIO.output(left_front, GPIO.LOW)
    if x != 0:
        time.sleep(x)
    return()

def leftturn(x=0.2):
    GPIO.output(right_front, GPIO.HIGH)
    GPIO.output(left_front, GPIO.LOW)
    GPIO.output(right_back, GPIO.LOW)
    GPIO.output(left_back, GPIO.LOW)
    time.sleep(x)  # 路面状況などによって時間調整
    stop()
    return()


def rightturn(x=0.2):
    GPIO.output(right_front, GPIO.LOW)
    GPIO.output(left_front, GPIO.HIGH)
    GPIO.output(right_back, GPIO.LOW)
    GPIO.output(left_back, GPIO.LOW)
    time.sleep(x)  # 路面状況などによって時間調整
    stop()
    return()


def leftbackturn(x=1):
    GPIO.output(left_back, GPIO.HIGH)
    GPIO.output(right_back, GPIO.LOW)
    GPIO.output(left_front, GPIO.LOW)
    GPIO.output(right_back, GPIO.LOW)
    time.sleep(x)
    stop()
    return()


def rightbackturn(x=1):
    GPIO.output(left_back, GPIO.LOW)
    GPIO.output(right_back, GPIO.HIGH)
    GPIO.output(left_front, GPIO.LOW)
    GPIO.output(right_front, GPIO.LOW)
    time.sleep(x)
    stop()
    return()


def leftspin(x=1):
    GPIO.output(right_front, GPIO.HIGH)
    GPIO.output(left_front, GPIO.LOW)
    GPIO.output(right_back, GPIO.LOW)
    GPIO.output(left_back, GPIO.HIGH)
    time.sleep(1)
    stop()
    return()


def rightspin(x=1):
    GPIO.output(right_front, GPIO.LOW)
    GPIO.output(left_front, GPIO.HIGH)
    GPIO.output(right_back, GPIO.HIGH)
    GPIO.output(left_back, GPIO.LOW)
    time.sleep(1)
    stop()
    return()


def wave(x):  # continuous back and forward
    for i in range(x):
        GPIO.output(right_back, GPIO.HIGH)
        GPIO.output(left_back, GPIO.HIGH)
        GPIO.output(right_front, GPIO.LOW)
        GPIO.output(left_front, GPIO.LOW)
        time.sleep(1)
        GPIO.output(right_front, GPIO.HIGH)
        GPIO.output(left_front, GPIO.HIGH)
        GPIO.output(right_back, GPIO.LOW)
        GPIO.output(left_back, GPIO.LOW)
        time.sleep(1)
    return()


def sign_on():
    GPIO.output(green_led, GPIO.HIGH)
    return()


def sign_off():
    GPIO.output(green_led, GPIO.LOW)
    return()


def burning(burningtime):
    GPIO.output(nicr_burn, GPIO.HIGH)
    time.sleep(burningtime)
    GPIO.output(nicr_burn, GPIO.LOW)
    return()


def escape1(runtime):  # reforward(x):  # back and forward
    GPIO.output(right_back, GPIO.HIGH)
    GPIO.output(left_back, GPIO.HIGH)
    GPIO.output(right_front, GPIO.LOW)
    GPIO.output(left_front, GPIO.LOW)
    time.sleep(runtime)
    GPIO.output(right_front, GPIO.HIGH)
    GPIO.output(left_front, GPIO.HIGH)
    GPIO.output(right_back, GPIO.LOW)
    GPIO.output(left_back, GPIO.LOW)
    time.sleep(5)
    return()


def escape2(runtime=0):  # 左輪乗り上げたときの脱出
    leftbackturn(1)
    back(3)
    stop()
    return()


def escape3(runtime=0):  # 右輪乗り上げたときの脱出
    rightbackturn(1)
    back(3)
    stop()
    return()


def escape4(runtime=1):  # 転倒したとき・スタックしたとき両方に有効
    leftspin(runtime)
    forward(2)
    stop()
    return()


def escape5(runtime=1):  # 転倒したとき・スタックしたとき両方に有効
    rightspin(runtime)
    forward(2)
    stop()
    return()


def escape6(runtime=1):  # 転倒したときの復帰に最適 まずこれを試す
    back(runtime)
    forward(2)
    stop()
    return()


def escape7(runtime=1):  # 転倒したとき・スタックしたとき両方に有効
    leftbackturn(runtime)
    back(1)
    forward(2)
    stop()
    return()


def escape8(runtime=1):  # 転倒したとき・スタックしたとき両方に有効
    rightbackturn(runtime)
    back(1)
    forward(2)
    stop()
    return()


def escape9(runtime=1):  # 転倒したとき・スタックしたとき両方に有効
    leftspin(runtime)
    back(1)
    forward(2)
    stop()
    return()


def escape10(runtime=1):  # 転倒したとき・スタックしたとき両方に有効
    rightspin(runtime)
    back(1)
    forward(2)
    stop()
    return()


def stack(pattern, runtime):  # stack用 pattern<=10
    if pattern == 1:
        escape1(runtime)
    if pattern == 2:
        escape2(runtime)
    if pattern == 3:
        escape3(runtime)
    if pattern == 4:
        escape4(runtime)
    if pattern == 5:
        escape5(runtime)
    if pattern == 6:
        escape6(runtime)
    if pattern == 7:
        escape7(runtime)
    if pattern == 8:
        escape8(runtime)
    if pattern == 9:
        escape9(runtime)
    if pattern == 10:
        escape10(runtime)


def turnrecover(pattern, runtime):  # turnrecover用 pattern<=5
    if pattern == 1:
        escape4(runtime)
    if pattern == 2:
        escape5(runtime)
    if pattern == 3:
        escape6(runtime)
    if pattern == 4:
        escape7(runtime)
    if pattern == 5:
        escape8(runtime)


def randomstack(pattern, runtime):  # random用 pattern<=19
    if pattern == 1:
        forward(runtime)
    if pattern == 2:
        back(runtime)
    if pattern == 3:
        leftturn(runtime)
    if pattern == 4:
        rightturn(runtime)
    if pattern == 5:
        leftbackturn(runtime)
    if pattern == 6:
        rightbackturn(runtime)
    if pattern == 7:
        leftspin(runtime)
    if pattern == 8:
        rightspin(runtime)
    if pattern == 9:
        escape1(runtime)
    if pattern == 10:
        escape2(runtime)
    if pattern == 11:
        escape3(runtime)
    if pattern == 12:
        escape4(runtime)
    if pattern == 13:
        escape4(runtime)
    if pattern == 14:
        escape5(runtime)
    if pattern == 15:
        escape6(runtime)
    if pattern == 16:
        escape7(runtime)
    if pattern == 17:
        escape8(runtime)
    if pattern == 18:
        escape9(runtime)
    if pattern == 19:
        escape10(runtime)
