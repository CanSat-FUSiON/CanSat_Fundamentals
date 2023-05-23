import math
import json


class Sensor:
    def __init__(self, i2c, sensor, gps_socket, data_stream, lastval, offset_mag_x, offset_mag_y, offset_mag_degree):
        self.i2c = i2c
        self.sensor = sensor
        self.gps_socket = gps_socket
        self.data_stream = data_stream
        self.lastval = lastval
        self.offset_mag_x = offset_mag_x
        self.offset_mag_y = offset_mag_y
        self.offset_mag_degree = offset_mag_degree

    def set_gps(self):
        self.lat, self.lon = self.gpsget()

    def set_mag(self):
        self.mag_x, self.mag_y, self.mag_z = self.getmag()

    def set_acc(self):
        self.acc_x, self.acc_y, self.acc_z = self.getacc()

    def gpsget(self):
        try:
            gps_dict = {
                "time": "n/a",
                "lat": "n/a",
                "lon": "n/a",
            }
            for new_data in self.gps_socket:
                if not new_data:
                    continue

                new_data_dict = json.loads(new_data)
                if new_data_dict["class"] != "TPV":
                    continue

                # ref: https://github.com/wadda/gps3/blob/master/gps3/gps3.py
                self.data_stream.unpack(new_data)
                if self.data_stream.TPV["time"] == "n/a":
                    continue

                gps_dict = {
                    "time": self.data_stream.TPV["time"],
                    "lat": self.data_stream.TPV["lat"],
                    "lon": self.data_stream.TPV["lon"],
                }
                break

            lat_i = gps_dict["lat"]
            lon_i = gps_dict["lon"]
            return (lat_i, lon_i)

        except:
            lat_i = 0
            lon_i = 0
            return (lat_i, lon_i)

    def getmag(self):
        [mag_x, mag_y, mag_z] = self.sensor.magnetic
        mag_x = mag_x - self.offset_mag_x
        mag_y = mag_y - self.offset_mag_y
        return (mag_x, mag_y, mag_z)

    def getacc(self):
        [accel_x, accel_y, accel_z] = self.sensor.acceleration
        return (accel_x, accel_y, accel_z)

    def rad_magnet(self):
        rad = math.atan2(self.mag_y, self.mag_x)
        return rad
