# -*- coding: utf-8 -*-
from time import sleep
import glob
import requests
import BMP085 as BMP085

class Api:
    url = "https://api.nag-iot.zcu.cz/v2/value/"

    def __init__(self, key):
        self.apiKey = key
        self.headers = {'content-type': 'application/json', 'x-api-key': key}
        self.params = {'api_key': key}

    def send_data(self, value, var):
        url = self.url + var
        requests.post(url, params=self.params, json={'value': value})
        

def read_temp():
    one_wire_dir = '/sys/bus/w1/devices/'
    device_dir = glob.glob(one_wire_dir + '28*')[0]
    device_file = device_dir + '/w1_slave'
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


# Funkce, která vrátí teplotu senzoru dallas

def get_temp():
    lines = read_temp()
    # cekani dokud neni senzor dostupny
    while lines[0].strip()[-3:] != 'YES':
        sleep(0.2)
        lines = read_temp()
    equals_pos = lines[1].find('t=')
    # ziskani teploty se souboru
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c                                                                                                    


api = Api('Ee9awVdZMkgea2ht')
sensor = BMP085.BMP085()


def sensors_loop():
    try:
        while True:
            temp = get_temp()
            pressure = sensor.read_pressure()
            print("Temperature: " + str(temp) + u" °C ")
            api.send_data(temp, "temp")
            print("Pressure: " + str(pressure) + " Pa")
            api.send_data(pressure, "pressure")
            sleep(60)
    finally:
        sensors_loop()

sensors_loop()
