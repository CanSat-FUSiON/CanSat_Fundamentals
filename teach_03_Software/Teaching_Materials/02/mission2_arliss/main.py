from motor import Motor
from longsleep import Longsleep
from step import Step
from camerarun import Camerarun
from logs import Logs
from stack import Stackrun
from stack import Gpsstack
from stack import Accstack
from communication import Communicator
from gpsrunner import Gpsrunner
from sensor import Sensor
from landingdetecter import Landingdetecter
from geopy.distance import geodesic
import os
import smbus
from itertools import count
import csv
from gps3 import gps3
from time import sleep
import RPi.GPIO as GPIO
import LPS25HB
import board
import adafruit_bno055
import math
from readline import set_completion_display_matches_hook
from socket import MSG_WAITALL
from tokenize import Double
from adafruit_extended_bus import ExtendedI2C as I2C
import runpattern
import sys
sys.path.insert(4, '/home/pi/.local/lib/python3.7/site-packages')


# import random
# import time
# import serial
# from multiprocessing.connection import wait
# import multiprocessing
# import datetime

# import picamera
# import picamera.array
# import cv2 as cv
# import numpy as np

runpattern.first()


def main():
    try:
        runpattern.first()  # ピンが最初に回ってしまう(クソ)問題の解決法。(詳しくはrunpatten.pyへ)
        step = Step()  # Step(Class)のインスタンスを作成。あらゆるタイマーはこのインスタンスの値で条件分岐する。
        step.set_longsleep_steptime()  # longsleeptimeを現在時刻(起動時)に設定。
        gps_setting_socket = gps3.GPSDSocket()  # GPS情報をやり取りするインスタンスを作成。
        gps_setting_socket.connect()
        gps_setting_socket.watch()

        logs = Logs()  # Log(Class)のインスタンスを作成。あらゆるlogはこのインスタンスを通して書き込まれる。
        communication = Communicator(bus=smbus.SMBus(
            1), logclass=logs, gps_socket=gps_setting_socket, data_stream=gps3.DataStream())  # 通信をするためのCommunicator(Class)のインスタンスを作成。

        landingdetect = Landingdetecter(  # Landingdetecter(Class)のインスタンスを作成。
            time_limit=0, burn_time=10, hlist=[0, 1, 2, 3, 4])

        longsleep = Longsleep(file_name='sleeptime', encoding='UTF-8',  # Longsleep(Class)のインスタンスを作成。
                              fr_time=0, com_time=0, ld_time=0, pt_time=10)  # 初期設定。pt_timeを10で設定しておく。

        sensor = Sensor(i2c=I2C(1), sensor=adafruit_bno055.BNO055_I2C(I2C(1)), gps_socket=gps_setting_socket,  # Sensor(Class)のインスタンスを作成。
                        data_stream=gps3.DataStream(), lastval=0xFFFF, offset_mag_x=0, offset_mag_y=0, offset_mag_degree=0)
        gpsrunner = Gpsrunner(goal_lat=40.900522, goal_lon=-119.07909722,  # Gpsrunner(Class)のインスタンスを作成。
                              radius_Earth=6378137., THRESHOLD=15, distance_THR=1.2, pitch_time=1)
        accstack = Accstack(ygradlist=[0, 0, 0, 0, 0, 0],  # Accstack(Class)のインスタンスを作成。
                            startstack_THR=15, finishstack_THR=10, turnover_THR=-5, pitch_time=30, ygradoffset=6)
        gpsstack = Gpsstack(GPS_stack_radius=3, latlist=[200, 300, 400, 500], lonlist=[  # Gpsstack(Class)のインスタンスを作成。
                            200, 300, 400, 500], latrate=111015.4872, lonrate=89925.9685, pitch_time=60)
        stackrun = Stackrun()  # Stackrun(Class)のインスタンスを作成。
        camerarun = Camerarun(resolution=(512, 384), framerate=10,  # Camerarun(Class)のインスタンスを作成。
                              occ_THR_low=0.005, occ_THR_high=0.1, range_THR=200, pt_time=5)
        motor = Motor()  # Motor(Class)のインスタンスを作成。

        while True:
            # com_timeは通信を始める時間(comunicate)。これを0としている。ループでカウントダウンが減り続けて0を下回るとbreakする。
            if int(longsleep.cd_time) <= int(longsleep.com_time):
                break
            runpattern.sign_on()  # LEDの操作。longsleep.pt_timeは LEDが点滅する時間*2 & 判定のループインターバル。
            sleep(longsleep.pt_time/2)
            runpattern.sign_off()
            sleep(longsleep.pt_time/2)

            # 1ループ後からlongsleep.pt_timeを超えたらカウントダウンが更新される。
            if step.evaluate_longsleep_steptime().seconds >= longsleep.pt_time:  # 1ループでpt_timeを超えるとcd_timeを更新する(ifは予防線)。
                longsleep.set()  # txtを通してtt_timeを更新する。
                longsleep.rewrite()  # txtを更新(次のループのために)

                # ↑なぜこんなことをしているのか？これは途中でコードが止まり、再起動などが入ってしまった時の予防策。(他の方法があるなら変えたほうがいい)
                # 再起動されてしまうとlongsleepの時間が更新されないため、また1から始まってしまう。
                # そのため、どこまで進んだかの情報(tt_time)を他の媒体(***.txt)に記憶させることで、再起動しても途中からコードをスタートできる。

                print(longsleep.cd_time)
                step.set_longsleep_steptime()

        # communication.gpsget_com_first()
        communication.start()  # 通信開始。

        while True:
            if int(longsleep.cd_time) <= int(longsleep.ld_time):  # ほぼ上のループと似たような考え方。
                break
            if step.evaluate_longsleep_steptime().seconds >= longsleep.pt_time:
                longsleep.set()
                longsleep.rewrite()
                print(longsleep.cd_time)
                step.set_longsleep_steptime()

        step.set_landing_steptime()  # ここから着地判定を始める。着地判定でもタイマーを設定するため、ここで0時間を設定する。

        while True:
            if int(longsleep.cd_time) <= -1:  # 再起動した際の予防線。
                break
            else:
                if step.evaluate_landing_steptime().seconds + step.evaluate_landing_steptime().microseconds/1000000 > 0.5:
                    landingdetect.set()
                    landingdetect.detect()
                    landingdetect.measureprint()
                    step.set_landing_steptime()
                if step.evaluate_longsleep_steptime().seconds >= longsleep.pt_time:
                    longsleep.set()
                    longsleep.rewrite()
                    print(longsleep.cd_time)
                    step.set_longsleep_steptime()
                if landingdetect.detectsign == 1 or longsleep.cd_time == 0:
                    landingdetect.warning()
                    landingdetect.nicrburn()
                    print("start burning")
                    sleep(5)
                    landingdetect.finish_run(runtime=5)
                    print("open")
                    runpattern.stop()
                    break

        longsleep.cd_time = -1  # 再起動したらburningの工程を無視して進む。
        longsleep.rewrite()

        while True:
            step.set_gpsrun_steptime()  # それぞれの時間を初期化。
            step.set_gpsstack_steptime()
            step.set_accstack_steptime()

            while True:
                print("start GPSrun")
                sensor.set_gps()  # それぞれの情報を取ってくる。
                sensor.set_mag()
                sensor.set_acc()
                gpsrunner.set(sensor)  # センサーの値を使って制御を行う。
                gpsrunner.gpsrun_print()  # 一応どう進めるかをprintする。
                # GPS走行である距離(閾値)まで近づいていたかを確認する。
                if gpsrunner.distance_ntg <= gpsrunner.distance_THR:
                    gpsrunner.gpsrunfinish()
                    break
                if step.evaluate_gpsrun_steptime().seconds >= gpsrunner.pitch_time:  # pitchタイムを超えるとlogを残す。
                    gpsrunner.gpsrun(motor)
                    logs.con_log(gpsrunner.loglist)
                    step.set_gpsrun_steptime()
                # stackを判定するaccstack.pitch_timeを超えるとスタックの判定をはじめる。
                if step.evaluate_accstack_steptime().seconds+step.evaluate_accstack_steptime().microseconds/1000000 >= accstack.pitch_time:
                    accstack.set(sensor)
                    print(accstack.ygradlist)
                    print(accstack.acc_z)
                    if accstack.acc_z <= accstack.turnover_THR:  # スタックの判定とそのあとの操作。
                        accstack.startprint()
                        runpattern.stack(pattern=4, runtime=1)
                        sensor.set_acc()
                        accstack.set(sensor)
                        accstack.nowprint()
                        sleep(1)
                        if accstack.acc_z <= accstack.turnover_THR:
                            while True:
                                stackrun.set(pattern_range=[
                                    12, 19], runtime_range=[1, 10])  # ランダムなパターンで走行を行う。
                                stackrun.escaperun()
                                sensor.set_acc()
                                accstack.set(sensor)
                                accstack.nowprint()
                                sleep(1)
                                if accstack.acc_z >= accstack.turnover_THR:  # スタック状態を抜けたかどうか判定。
                                    break
                    step.set_accstack_steptime()
                # GPSによるスタック判定を行うインターバル時間を超えたらGPSスタック判定をおこなう。GPSによるstack判定とは、あまりにGPSの値に変化がなかった場合に始める判定のこと。
                if step.evaluate_gpsstack_steptime().seconds >= gpsstack.pitch_time:
                    gpsstack.set(sensor)
                    print(gpsstack.dif_abs_m)
                    print(gpsstack.latlist)
                    if gpsstack.dif_abs_m <= gpsstack.GPS_stack_radius:
                        gpsstack.startprint()
                        while True:
                            stackrun.set(pattern_range=[
                                         1, 19], runtime_range=[2, 6])
                            stackrun.escaperun()
                            sensor.set_gps()
                            gpsstack.set_diflist(sensor)
                            gpsstack.nowprint()
                            sleep(1)
                            if min(gpsstack.diflist) > gpsstack.GPS_stack_radius:
                                gpsstack.finishprint()
                                gpsstack.set_latlist(  # 問題のない値に初期化。
                                    latlist=[200, 300, 400, 500])
                                gpsstack.set_lonlist(  # 問題のない値に初期化。
                                    lonlist=[200, 300, 400, 500])
                                break
                    step.set_gpsstack_steptime()
                sleep(0.5)

            step.set_imagesave_steptime()  # 画像処理開始。
            step.set_accstack_steptime()
            step.set_error_steptime()

            while True:
                camerarun.getdata()
                camerarun.run(motor)
                logs.cam_log(camerarun.loglist)
                if step.evaluate_imagesave_steptime().seconds >= camerarun.pt_time:
                    camerarun.save()
                    step.set_imagesave_steptime()
                if step.evaluate_accstack_steptime().seconds >= camerarun.pt_time:
                    sensor.set_acc()
                    accstack.set(sensor)
                    if accstack.acc_z <= accstack.turnover_THR:
                        accstack.startprint()
                        runpattern.stack(pattern=4, runtime=1)
                        sensor.set_acc()
                        accstack.set(sensor)
                        accstack.nowprint()
                        sleep(1)
                        if accstack.acc_z <= accstack.turnover_THR:
                            while True:
                                stackrun.set(pattern_range=[
                                    12, 19], runtime_range=[1, 10])
                                stackrun.escaperun()
                                sensor.set_acc()
                                accstack.set(sensor)
                                accstack.nowprint()
                                sleep(1)
                                if accstack.acc_z >= accstack.turnover_THR:
                                    break
                    step.set_accstack_steptime()
                if step.evaluate_error_steptime().seconds > 60:
                    sensor.set_gps()
                    gpsrunner.set(sensor)
                if camerarun.jd_sign == 2 or gpsrunner.distance_ntg > gpsrunner.distance_THR:
                    break

            if camerarun.jd_sign == 2:
                break

            else:
                pass

        # communication.stop()
        gps_setting_socket.close()

        while True:
            sleep(10)

    except KeyboardInterrupt:
        longsleep.cd_time = longsleep.fr_time
        longsleep.rewrite()


while True:
    try:
        main()
        break
    except KeyboardInterrupt:
        runpattern.stop()
        GPIO.cleanup()
    except:
        pass
