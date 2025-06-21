from gps3 import gps3
import utilities as ut
import math
from geopy.distance import geodesic
import runpattern


class Gpsrunner:
    def __init__(self, goal_lat, goal_lon, radius_Earth, THRESHOLD, distance_THR, pitch_time=1):
        self.goal_lat = goal_lat
        self.goal_lon = goal_lon
        self.radius_Earth = radius_Earth
        self.THRESHOLD = THRESHOLD
        self.distance_THR = distance_THR
        self.pitch_time = pitch_time

    def set(self, rawvalue):
        self.lat = rawvalue.lat
        self.lon = rawvalue.lon
        self.now_x = self.get_nowx()
        self.now_y = self.get_nowy()
        self.polar_ntg = self.get_polarntg()
        self.deg_ntg = self.get_degntg()
        self.distance_ntg = self.get_distancentg()
        self.mag_x = rawvalue.mag_x
        self.mag_y = rawvalue.mag_y
        self.mag_z = rawvalue.mag_z
        self.acc_x = rawvalue.acc_x
        self.acc_y = rawvalue.acc_y
        self.acc_z = rawvalue.acc_z
        self.offset_mag_degree = rawvalue.offset_mag_degree
        self.arg_degree = self.get_arg_degree()
        self.orient = self.get_orient()
        self.control_sign = self.gpscontrol()
        self.loglist = [self.lat, self.lon,
                        math.sin(math.radians(self.arg_degree)), math.cos(math.radians(self.arg_degree)), self.control_sign]

    def radworld(self):
        length_world = self.radius_Earth * math.cos(math.radians(self.lat))
        return length_world

    def get_nowx(self):
        now_x = self.radworld() * math.radians(self.goal_lon-self.lon)
        return now_x

    def get_nowy(self):
        now_y = self.radius_Earth * math.radians(self.goal_lat - self.lat)
        return now_y

    def get_polarntg(self):
        polar_ntg = math.degrees(math.atan2(self.now_y, self.now_x))
        return polar_ntg

    def get_degntg(self):
        deg_ntg = 90 - self.polar_ntg
        if deg_ntg < 0:
            deg_ntg = deg_ntg + 360
        return deg_ntg

    def get_distancentg(self):
        distance_ntg = geodesic(
            (self.goal_lat, self.goal_lon), (self.lat, self.lon)).m
        return distance_ntg

    def _rad_magnet(self):
        rad = math.atan2(self.mag_y, self.mag_x)
        return rad

    def get_arg_degree(self):
        arg_degree = math.degrees(self._rad_magnet()) + self.offset_mag_degree
        if arg_degree < 0:
            arg_degree = arg_degree + 360
        return arg_degree

    def get_orient(self):
        if self.arg_degree < self.deg_ntg:
            arg_degree = self.arg_degree + 360
        else:
            arg_degree = self.arg_degree
        orient = arg_degree - self.deg_ntg
        return orient

    def gpscontrol(self):
        if 0 <= self.orient < self.THRESHOLD or (360 - self.THRESHOLD) < self.orient < 360:
            control_sign = 0
        elif (self.THRESHOLD) < self.orient <= (180):
            control_sign = 1
        elif (180) < self.orient <= (360-self.THRESHOLD):
            control_sign = 2
        return control_sign

    def gpsrun(self, motor):
        if self.control_sign == 0:
            motor.forward_gps()
        elif self.control_sign == 1:
            motor.left()
        elif self.control_sign == 2:
            motor.right()

    def gpsrunfinish(self):
        runpattern.stop()

    def gpsrun_print(self):
        print("\n----------------------")
        print("goal latitude:", self.goal_lat)
        print("goal lontitude:", self.goal_lon)
        print("\nlatitude:", self.lat)
        print("longitude:", self.lon)
        print("\ngoal direction:", self.deg_ntg)
        print("distance:", self.distance_ntg)
        print("\nmachine angle:", self.arg_degree)
        if self.control_sign == 0:
            print("\ncontrol: forward")
        elif self.control_sign == 1:
            print("\ncontrol: left")
        elif self.control_sign == 2:
            print("\ncontrol: right")
        print("----------------------")
