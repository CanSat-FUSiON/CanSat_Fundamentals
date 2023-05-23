import datetime


class Logs:
    def __init__(self):
        self.timezone = datetime.timezone(
            datetime.timedelta(hours=-7), name='US')
        self.flight_starttime = datetime.datetime.now(self.timezone)
        nm = str(str(self.flight_starttime.month)+'-'+str(self.flight_starttime.day)+'_' +
                 str(self.flight_starttime.hour)+':'+str(self.flight_starttime.minute)+':'+str(self.flight_starttime.second))
        self.connm = str('con_'+nm)  # file名を設定。ファイルが作られた時間がファイル名になっている。
        self.ffnm = str('ff_'+nm)
        self.camnm = str('cam_'+nm)

    def ff_log(self, loglist):  # from flightの意味。通信と一緒に動くので、GPSのデータを常に残し続ける。(GPS以外の情報も残そう・・・)
        f = open('/home/pi/Desktop/Mission2/2.ARLISS/expall/905/logs/'+self.ffnm+'.csv', "a")
        f.write(str(datetime.datetime.now(self.timezone)))
        for log in loglist:
            f.write(',')
            f.write(str(log))
        f.write('\n')
        f.close

    def con_log(self, loglist):  # 制御履歴を残すコード。
        f = open('/home/pi/Desktop/Mission2/2.ARLISS/expall/905/logs/'+self.connm+'.csv', "a")
        f.write(str(datetime.datetime.now(self.timezone)))
        for log in loglist:
            f.write(',')
            f.write(str(log))
        f.write("\n")
        f.close

    def cam_log(self, loglist):
        f = open('/home/pi/Desktop/Mission2/2.ARLISS/expall/905/logs/'+self.camnm+'.csv', "a")
        f.write(str(datetime.datetime.now(self.timezone)))
        for log in loglist:
            f.write(',')
            f.write(str(log))
        f.write('\n')
        f.close
