import requests
import os
from time import sleep

from dotenv import load_dotenv
import serial


def get_data(api_key: str, base: str, **kw):
    """Return JSON data from given request with given kwargs"""
    base_url = f"http://mbus.ltp.umich.edu/bustime/api/v3/{base}?key={api_key}&format=json"
    for key, value in kw.items():
        base_url += f"&{key}={value}"
    return requests.get(base_url).json()

def trigger_light(arduino, on=False):
    """Trigger the onboard LED on the Arduino whenever a bus approaches"""
    arduino.write(f"{"t" if on else "f"}".encode())


def main(api_key, arduino):
    while True: 
        bus_approaching = False
        prediction_data = get_data(api_key, "getpredictions", stpid = "C250")
        for prediction in prediction_data["bustime-response"]["prd"]:
            if prediction["typ"] == "A" and prediction["prdctdn"] == "DUE":
                print(f"Route {prediction["rt"]} due")
                bus_approaching = True
        trigger_light(arduino, bus_approaching)
        sleep(2)


if __name__ == "__main__":
    load_dotenv()
    API_KEY = os.environ['API_KEY']
    arduino = serial.Serial("/dev/cu.usbmodem11101", 9600, timeout=0.1)
    main(API_KEY, arduino)





