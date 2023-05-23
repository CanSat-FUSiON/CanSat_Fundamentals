import datetime


class Step:
    def __init__(self):  # タイムゾーンはアメリカの標準時に合わせる。
        self.timezone = datetime.timezone(
            datetime.timedelta(hours=-7), name='US')
        self.starttime = datetime.datetime.now(self.timezone)

    def set_all_steptime(self):  # とりあえずすべてのメンバの時間を合わせる。
        nowtime = datetime.datetime.now(self.timezone)
        self.longsleep_steptime = nowtime
        self.landing_steptime = nowtime
        self.gpsrun_steptime = nowtime
        self.gpsstack_steptime = nowtime
        self.accstack_steptime = nowtime
        self.imagesave_steptime = nowtime
        self.error_steptime = nowtime

    def set_longsleep_steptime(self):  # それぞれの時間を初期化したいタイミングで実行するメソッド。
        self.longsleep_steptime = datetime.datetime.now(self.timezone)

    def set_landing_steptime(self):
        self.landing_steptime = datetime.datetime.now(self.timezone)

    def set_gpsrun_steptime(self):
        self.gpsrun_steptime = datetime.datetime.now(self.timezone)

    def set_gpsstack_steptime(self):
        self.gpsstack_steptime = datetime.datetime.now(self.timezone)

    def set_accstack_steptime(self):
        self.accstack_steptime = datetime.datetime.now(self.timezone)

    def set_imagesave_steptime(self):
        self.imagesave_steptime = datetime.datetime.now(self.timezone)

    def set_error_steptime(self):
        self.error_steptime = datetime.datetime.now(self.timezone)

    def evaluate_runningtime(self):
        return (datetime.datetime.now(self.timezone) - self.starttime)

    def evaluate_longsleep_steptime(self):  # 起動を始めてからどれくらいの時間がたったのかを返す関数。
        return (datetime.datetime.now(self.timezone) - self.longsleep_steptime)

    def evaluate_landing_steptime(self):
        return (datetime.datetime.now(self.timezone) - self.landing_steptime)

    def evaluate_gpsrun_steptime(self):
        return (datetime.datetime.now(self.timezone) - self.gpsrun_steptime)

    def evaluate_gpsstack_steptime(self):
        return (datetime.datetime.now(self.timezone) - self.gpsstack_steptime)

    def evaluate_accstack_steptime(self):
        return (datetime.datetime.now(self.timezone) - self.accstack_steptime)

    def evaluate_imagesave_steptime(self):
        return (datetime.datetime.now(self.timezone) - self.imagesave_steptime)

    def evaluate_error_steptime(self):
        return (datetime.datetime.now(self.timezone) - self.error_steptime)
