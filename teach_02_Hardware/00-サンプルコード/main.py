# main.py の例
from led_module import LEDController
from button_module import Button
from pwm_module import BrightnessPWM
from print_module import SerialPrint

# ハードウェア初期化
led = LEDController(25)           # オンボードLED
button = Button(14)               # GPIO14にタクトスイッチ
pwm_led = BrightnessPWM(15)       # GPIO15に外部LED
printer = SerialPrint()

brightness_level = 0              # 明度レベル（0-5）

while True:
    if button.is_pressed():
        brightness_level = (brightness_level + 1) % 6  # 0-5でループ
        pwm_led.set_brightness(brightness_level * 20)  # 0%, 20%, 40%...100%
        printer.print(f"明度レベル: {brightness_level}, 明度: {brightness_level * 20}%")

        # 状態表示用LED点滅
        led.blink(brightness_level + 1, 0.2)  # レベル+1回点滅
