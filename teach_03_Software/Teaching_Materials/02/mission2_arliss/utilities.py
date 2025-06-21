from gps3 import gps3


def gpssetup_connect(gps_socket):
    gps_socket.connect()


def gpssetup_watch(gps_socket):
    gps_socket.watch()


def gpsdictget(data_stream, new_data):
    try:
        if new_data:
            data_stream.unpack(new_data)
            gps_dict = {"time": data_stream.TPV['time'],
                        "lat": data_stream.TPV['lat'],
                        "lon": data_stream.TPV['lon']}
        else:
            gps_dict = {"time": "n/a",
                        "lat": 0,
                        "lon": 0}
    except:
        gps_dict = {"time": "n/a",
                    "lat": 0,
                    "lon": 0}

    return gps_dict
