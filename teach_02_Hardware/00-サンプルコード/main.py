"""
main.py  –  基本 I/O 演習デモ
---------------------------------
* ボタンを押すたびに外付け LED の明るさを 0→20→…→100→0 % で循環
* 変化を UART(115200 bps) に出力
* 現在レベル+1 回、オンボード LED を点滅してフィードバック
対象: Raspberry Pi Pico (MicroPython v1.22 以降を想定)
"""

import time
from led_module import LEDController
from button_module import Button
from print_module import SerialPrint

# ─── ハード初期化 ────────────────────────────────────
status_led   = LEDController(pin_no=25)   # Pico オンボード LED (GP25)
bright_led   = LEDController(pin_no=15)   # 外付け LED (例: GP15)
button       = Button(pin_no=14)          # タクトスイッチ (GP14, 内部 Pull‑up)
uart_printer = SerialPrint()              # UART0/115200

brightness_level = 0           # 0〜5
STEP_PERCENT     = 20          # 1 段あたり 20 %

# ─── メインループ ───────────────────────────────────
while True:
    if button.is_pressed():
        # 1. 明るさレベル更新
        brightness_level = (brightness_level + 1) % 6   # 0→5→0…
        percent = brightness_level * STEP_PERCENT

        # 2. PWM デューティ変更
        bright_led.set_brightness(percent)

        # 3. シリアルに現在値を送信
        uart_printer.print(
            "Brightness level:", brightness_level,
            "(", percent, "% )"
        )

        # 4. 状態表示としてオンボード LED を点滅
        status_led.blink(times=brightness_level + 1, interval=0.2)

        # 押しっぱなし誤動作防止（チャタリング回避も兼ねて）
        while button.is_pressed():
            time.sleep(0.02)

    # CPU を休ませる（ポーリング周期 ≒10 ms）
    time.sleep(0.01)
