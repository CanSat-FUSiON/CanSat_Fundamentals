import queue
import math
import random
import morter_RUN


class Accstack:
    def __init__(self, ygradlist, startstack_THR, finishstack_THR, turnover_THR, pitch_time, ygradoffset):
        self.ygradlist = ygradlist
        self.startstack_THR = startstack_THR
        self.finishstack_THR = finishstack_THR
        self.turnover_THR = turnover_THR
        self.pitch_time = pitch_time
        self.ygradoffset = ygradoffset

    def set(self, rawvalue):
        if -0.1 < rawvalue.acc_x < 0:
            self.acc_x = -0.1
        elif 0 <= rawvalue.acc_x < 0.1:
            self.acc_x = 0.1
        else:
            self.acc_x = rawvalue.acc_x

        if -0.1 < rawvalue.acc_y < 0:
            self.acc_y = -0.1
        elif 0 <= rawvalue.acc_y < 0.1:
            self.acc_y = 0.1
        else:
            self.acc_y = rawvalue.acc_y

        if -0.1 < rawvalue.acc_z < 0:
            self.acc_z = -0.1
        elif 0 <= rawvalue.acc_z < 0.1:
            self.acc_z = 0.1
        else:
            self.acc_z = rawvalue.acc_z

        self.max_grad = self.get_maxgrad()
        self.vec_x = self.get_normalvector()[0]
        self.vec_y = self.get_normalvector()[1]
        self.vec_z = self.get_normalvector()[2]

        if -0.1 < self.vec_z < 0:
            self.vec_z = -0.1
        elif 0 <= self.vec_z < 0.1:
            self.vec_z = 0.1
        else:
            self.vec_z = self.get_normalvector()[2]

        self.x_grad = self.get_axisgrad()[0]
        self.y_grad = self.get_axisgrad()[1] - math.radians(self.ygradoffset)
        self.y_gradlist = self.ygradlist_slide()

    def get_maxgrad(self):
        max_grad = math.atan(
            math.sqrt(self.acc_x**2+self.acc_y**2)/abs(self.acc_z))
        return max_grad

    def get_normalvector(self):
        vec_x = -math.cos(math.pi/2-self.max_grad) * \
            (-self.acc_x)/math.sqrt(self.acc_x**2+self.acc_y**2)
        vec_y = -math.cos(math.pi/2-self.max_grad) * \
            (-self.acc_y)/math.sqrt(self.acc_x**2+self.acc_y**2)
        vec_z = math.sin(math.pi/2-self.max_grad)
        return [vec_x, vec_y, vec_z]

    def get_axisgrad(self):
        x_grad = math.atan(self.vec_x/self.vec_z)
        y_grad = math.atan(self.vec_y/self.vec_z)
        return [x_grad, y_grad]

    def ygradlist_slide(self):
        ygradlist = self.ygradlist
        ygradlist.insert(0, -math.degrees(self.y_grad))
        del ygradlist[6]
        return ygradlist

    def setygradlist(self, ygradlist):
        self.ygradlist = ygradlist

    def startprint(self):
        print("stack now by slope")

    def nowprint(self):
        print("\nnow grad:", -math.degrees(self.y_grad))

    def finishprint(self):
        print("escale rut")


class Gpsstack:
    def __init__(self,  GPS_stack_radius, latlist, lonlist, latrate, lonrate, pitch_time):
        self.GPS_stack_radius = GPS_stack_radius
        self.latlist = latlist
        self.lonlist = lonlist
        self.latrate = latrate
        self.lonrate = lonrate
        self.pitch_time = pitch_time

    def set(self, rawvalue):
        self.lat_i = rawvalue.lat
        self.lon_i = rawvalue.lon
        self.latlist = self.latlist_slide()
        self.lonlist = self.lonlist_slide()
        self.dif_lat_m = self.get_diflat_m()
        self.dif_lon_m = self.get_diflat_m()
        self.dif_abs_m = self.get_difabs_m()

    def latlist_slide(self):
        latlist = self.latlist
        latlist.insert(0, self.lat_i)
        del latlist[4]
        return latlist

    def lonlist_slide(self):
        lonlist = self.lonlist
        lonlist.insert(0, self.lon_i)
        del lonlist[4]
        return lonlist

    def get_diflat_m(self):
        dif_lat_m = (max(self.latlist)-min(self.latlist))*self.latrate
        return dif_lat_m

    def get_diflon_m(self):
        dif_lon_m = max(self.lonlist)-min(self.lonlist)*self.lonrate
        return dif_lon_m

    def get_difabs_m(self):
        dif_abs_m = math.sqrt(self.dif_lat_m**2 + self.dif_lon_m**2)
        return dif_abs_m

    def set_diflist(self, rawvalue):
        self.updatelat = rawvalue.lat
        self.updatelon = rawvalue.lon
        self.diflist = self.get_dif()

    def get_dif(self):
        dif_1 = math.sqrt(
            ((self.updatelat-max(self.latlist))*self.latrate)**2 + ((self.updatelon-max(self.lonlist))*self.lonrate)**2)
        dif_2 = math.sqrt(
            ((self.updatelat-max(self.latlist))*self.latrate)**2 + ((self.updatelon-min(self.lonlist))*self.lonrate)**2)
        dif_3 = math.sqrt(
            ((self.updatelat-min(self.latlist))*self.latrate)**2 + ((self.updatelon-max(self.lonlist))*self.lonrate)**2)
        dif_4 = math.sqrt(
            ((self.updatelat-min(self.latlist))*self.latrate)**2 + ((self.updatelon-min(self.lonlist))*self.lonrate)**2)
        return [dif_1, dif_2, dif_3, dif_4]

    def set_latlist(self, latlist):
        self.latlist = latlist

    def set_lonlist(self, lonlist):
        self.lonlist = lonlist

    def startprint(self):
        print("stack now by stop")

    def nowprint(self):
        print("\nnow lattitude:", self.updatelat)
        print("now longitude:", self.updatelon)
        print("travel distance", min(self.diflist))

    def finishprint(self):
        print("escale rut")


class Stackrun:
    def __init__(self):
        pass

    def set(self, pattern_range, runtime_range):
        self.pattern_range = pattern_range
        self.runtime_range = runtime_range

    def escaperun(self):
        pattern = random.randint(self.pattern_range[0], self.pattern_range[1])
        runtime = random.uniform(self.runtime_range[0], self.runtime_range[1])
        morter_RUN.randomstack(pattern, runtime)

    def winningrun(self):
        morter_RUN.forward(10)
