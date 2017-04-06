import requests

class TrainTime:

    station_api_keys = {
        'CAN':'22a291a72b0f9f2b7b608cd8534889f6',
        'TLY':'4012186a5be087a8f411daf617bfed0a',
        'CLT':'abf3ffe0d99676bc7955a9bd1af534de',
        'TIR':'2114ce48ee51f920765ee1d4a948cb6b'
    }

    bw_station_api_keys = {
        'CAN-TIR':'eba99e3d53fefc2a3c16eb5eddecb039',
        'TIR-CAN':'378039cad5777afd5722356d375daf4c',
        'CLT-CAN':'8d4699f8952a6064e7ba0b320f3816a4',
        'CAN-CLT':'27c597f2ef11e1ad92a3324e78aba19d'
    }

    def getTrainsFromStation(station_code):
        r = requests.post('http://www.hgapis.com/railapi/v1/livestn',
                          {'stn_code':station_code,
                           'api_key':TrainTime.station_api_keys[station_code],
                           'app_version':'1.0'})
        if r.content and len(r.content)>0:
            j = r.json()
            return j['trains'], j['timestamp']
        else:
            return None,None
    def getTrainsBwStations(stations_code):
        stns = stations_code.split('-')
        fs = stns[0]
        ts = stns[1]
        r = requests.post('http://www.hgapis.com/railapi/v1/trainsbw',
                          {'fscode':fs,
                           'tscode':ts,
                           'api_key':TrainTime.bw_station_api_keys[stations_code],
                           'app_version':'1.0'})
        if r.content and len(r.content)>0:
            j = r.json()
            return j['trains'], j['timestamp']
        else:
            return None,None

    def getAvailableStations():
        return TrainTime.station_api_keys.keys()
    def getAvailableBwStations():
        return TrainTime.bw_station_api_keys.keys()
