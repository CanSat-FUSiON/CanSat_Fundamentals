import LPS25HB
import RPi.GPIO as GPIO
import morter_RUN
import time
import datetime


class Landingdetecter:
    def __init__(self, time_limit, burn_time, hlist):
        self.time_limit = time_limit
        self.burn_time = burn_time
        self.hlist = hlist
        self.led_sign = 0
        self.starttime = datetime.datetime.today()
        self.nowtime = datetime.datetime.today()
        self.detectsign = 0

    def set(self):
        self.nowtime = datetime.datetime.today()
        self.detectingtime = (self.nowtime - self.starttime).seconds + \
            (self.nowtime - self.starttime).microseconds/1000000
        self.height = self.get_height()
        self.hlist = self.hlistslide()
        self.diflist = self.get_diflist()

    def get_height(self):
        LPS25HB.enableDefault()
        temp = LPS25HB.readTemperatureC()
        pres = LPS25HB.readPressureMillibars()
        P0 = 1013.25
        height = ((P0/pres) ** (1/5.257)-1)*(temp+273.15)/0.0065
        return height

    def ledflashing(self):
        if self.led_sign == 0:
            morter_RUN.sign_on()
            self.led_sign = 1
        elif self.led_sign == 1:
            morter_RUN.sign_off()
            self.led_sign = 0

    def hlistslide(self):
        hlist = self.hlist
        hlist.insert(0, self.height)
        del hlist[5]
        return hlist

    def get_diflist(self):
        hlist = self.hlist
        dif0 = abs(hlist[1] - hlist[0])
        dif1 = abs(hlist[2] - hlist[1])
        dif2 = abs(hlist[3] - hlist[2])
        dif3 = abs(hlist[4] - hlist[3])
        return [dif0, dif1, dif2, dif3]

    def warning(self):
        danger = 0
        while danger <= 25:
            morter_RUN.sign_off()
            time.sleep(0.1)
            morter_RUN.sign_on()
            time.sleep(0.1)
            danger = 1+danger

    def detect(self):
        if max(self.diflist) < 0.1 or self.detectingtime > self.time_limit:
            self.detectsign = 1

    def nicrburn(self):
        morter_RUN.burning(self.burn_time)

    def finish_run(self,runtime):
        morter_RUN.forward(runtime)
        morter_RUN.stop()

    def measureprint(self):
        print("\n---------------")
        print("detectingtime:", self.detectingtime)
        print("\nheight:", self.height)
        if self.detectsign != 1:
            print("\nresult: not detect")
        elif self.detectsign == 0:
            print("\nresult: detect")
        print("---------------")
