import picamera
import picamera.array
import mdlreddetect as r
import morter_RUN
import datetime


class Camerarun:
    def __init__(self, resolution, framerate, occ_THR_low, occ_THR_high, range_THR, pt_time):
        self.resolution = resolution
        self.framerate = framerate
        self.occ_THR_low = occ_THR_low
        self.occ_THR_high = occ_THR_high
        self.range_THR = range_THR
        self.pt_time = pt_time
        self.savesign = 0

    def getdata(self):
        with picamera.PiCamera() as camera:
            with picamera.array.PiRGBArray(camera) as stream:
                self.savesign = (self.savesign + 1) % 5
                camera.resolution = self.resolution
                camera.framerate = self.framerate
                camera.capture(stream, 'bgr', use_video_port=True)
                self.occ = r.occ_get(stream.array)
                self.cen_x = r.size_get(stream.array)[
                    0]/2 - r.center_get(stream.array)[0]
                self.cen_y = r.center_get(stream.array)[1]
                self.jd_sign = self.judge_distance()
                self.jc_sign = self.judge_control()
                self.loglist = [self.occ, self.cen_x,
                                self.jd_sign, self.jc_sign]
                stream.seek(0)
                stream.truncate()

    def judge_distance(self):
        print(self.occ)
        if self.occ < self.occ_THR_low:
            print('can not find')
            return 0
        elif self.occ >= self.occ_THR_low and self.occ < self.occ_THR_high:
            print('can find')
            return 1
        else:
            print('goal')
            return 2

    def judge_control(self):
        print(self.cen_x)
        if -self.range_THR <= self.cen_x <= self.range_THR:
            return 0
        if self.cen_x > self.range_THR:
            return 1
        if self.cen_x < -self.range_THR:
            return 2

    def run(self, motor):
        if self.jd_sign == 0:
            motor.left()
        elif self.jd_sign == 1:
            if self.jc_sign == 0:
                motor.forward_cam()
                print("run forward")
            elif self.jc_sign == 1:
                motor.right()
                print("run right")
            else:
                motor.left()
                print("run left")
        else:
            morter_RUN.forward(1)
            morter_RUN.stop()

    def save(self):
        with picamera.PiCamera() as camera:
            camera.resolution = self.resolution
            US = datetime.timezone(datetime.timedelta(hours=-7), name='US')
            camera.capture('/home/pi/Desktop/Mission2/2.ARLISS/expall/905/images/' + str(datetime.datetime.now(US)) + '.jpg')
