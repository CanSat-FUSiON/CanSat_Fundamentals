import utilities as ut
import math
import time
import multiprocessing
import smbus
import json


class Communicator:
    def __init__(self, bus, logclass, gps_socket, data_stream):
        self.bus = bus
        self.logclass = logclass  # logを残すためのクラスをこちらに代入。
        self.gps_socket = gps_socket
        self.data_stream = data_stream
        self.lat_i = 0  # 初めはとりあえず緯度経度を0としておく。
        self.lon_i = 0
        self.loglist = [0, 0]  # リストでも緯度経度を保存するためのメンバ(容量の無駄だが・・・)。
        # 初めのセッティングでマルチプロセスの関数をメンバに入れている。(multi_running_communicationへ)
        self.commrunning = self.multi_running_communication()

    def communication(self):  # 通信で８桁ずつ数値を送るために情報を変更してる(とても頭の悪いやり方)。
        lat_1 = math.floor(self.lat_i)
        lat_2 = math.floor(self.lat_i*100 - lat_1*100)
        lat_3 = math.floor(self.lat_i*10000 - lat_1*10000 - lat_2*100)
        lat_4 = round(self.lat_i*1000000 - lat_1 *
                      1000000 - lat_2*10000 - lat_3*100)
        lon_1 = math.floor(self.lon_i)
        lon_2 = math.floor(self.lon_i*100 - lon_1*100)
        lon_3 = math.floor(self.lon_i*10000 - lon_1*10000 - lon_2*100)
        lon_4 = round(self.lon_i*1000000 - lon_1 *
                      1000000 - lon_2*10000 - lon_3*100)

        bus = self.bus  # 呪文。
        bus.write_byte(0x41, lat_1)  # データを送信。
        bus.write_byte(0x41, lat_2)
        bus.write_byte(0x41, lat_3)
        bus.write_byte(0x41, lat_4)
        bus.write_byte(0x41, lon_1)
        bus.write_byte(0x41, lon_2)
        bus.write_byte(0x41, lon_3)
        bus.write_byte(0x41, lon_4)

    def gpsget_com_first(self):  # 使ってないっぽい。負の遺産。
        gps_dict = {
            "time": "n/a",
            "lat": "n/a",
            "lon": "n/a",
        }
        for new_data in self.gps_socket:
            if not new_data:
                continue

            self.data_stream.unpack(new_data)
            if self.data_stream.TPV["time"] == "n/a":
                continue

            gps_dict = {
                "time": self.data_stream.TPV["time"],
                "lat": self.data_stream.TPV["lat"],
                "lon": self.data_stream.TPV["lon"],
            }
            break

        if gps_dict["time"] != "n/a":
            self.lat_i = gps_dict["lat"]
            self.lon_i = gps_dict["lon"]
            self.loglist = [self.lat_i, self.lon_i]
            self.communication()

    # GPSの値を取ってくるところ。GPS走行では制御内でGPSの値を取るコードが走る(sensor.py参照)が、通信はそれより手前のフェーズからデータを取ってくる必要があるので、別でGPSの値を取るコードを作成している。
    # 本来は制御におけるデータ取得と統合させたいところ(同じようなコードが2つ存在していることが美学に反するので笑)
    def gpsget_com(self):
        try:
            gps_dict = {
                "time": "n/a",
                "lat": "n/a",
                "lon": "n/a",
            }
            for new_data in self.gps_socket:  # GPSの値を取ってくるまで回すループ。
                if not new_data:
                    continue

                new_data_dict = json.loads(new_data)
                if new_data_dict["class"] != "TPV":
                    continue

                # ref: https://github.com/wadda/gps3/blob/master/gps3/gps3.py ← こちらを参考に。
                self.data_stream.unpack(new_data)
                if self.data_stream.TPV["time"] == "n/a":
                    continue

                gps_dict = {  # うまくとって来られたら代入。
                    "time": self.data_stream.TPV["time"],
                    "lat": self.data_stream.TPV["lat"],
                    "lon": self.data_stream.TPV["lon"],
                }
                break

            self.lat_i = gps_dict["lat"]
            self.lon_i = -gps_dict["lon"]  # 細かいが西経のため値が負。こういうことはやってみないと気づかないのでコードを動かす際は細かく確認すること。「論よりrun」
            self.loglist = [self.lat_i, self.lon_i]  # GPSの値から緯度経度の値をメンバに代入。
            self.communication()
        except:  # エラーが出て止まったら地上局側で知りたい。そのため0の値を返すように設定している。
            self.lat_i = 0
            self.lon_i = 0
            self.loglist = [self.lat_i, self.lon_i]
            self.communication()

    def running(self):
        while True:
            self.gpsget_com()  # gpsget_comというメソッドを開始。
            if self.loglist != [0, 0]:
                self.logclass.ff_log(self.loglist)  # ファイルにlogのデータを書き込む。
            time.sleep(2)

    # プロセスを2つ平行に進めるためのもの。通信と制御は一緒に行う必要がある。もし片方が止まったらもう一方も止まるという設計だと困るため。
    def multi_running_communication(self):
        # runningというメッセージを並行で処理しろよという命令。(並行処理は基本的にあまりお勧めされません。)runningへ。
        commrunning = multiprocessing.Process(target=self.running)
        return commrunning

    def start(self):  # 通信を始める。
        self.commrunning.start()

    def stop(self):  # 通信を終わらせる。
        self.commrunning.terminate()
