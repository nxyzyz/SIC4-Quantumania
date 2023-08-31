import time
import requests
import math
import random

TOKEN = "BBFF-fPfDBOehsSXEeYaLipQ5b71UrUOUam"  # Put your TOKEN here
DEVICE_LABEL = "ultrasonic111"  # Put your device label here 
VARIABLE_LABEL_1 = "ultrasonic1"  # Put your first variable label here
VARIABLE_LABEL_2 = "ultrasonic2"  # Put your second variable label here
VARIABLE_LABEL_3 = "ultrasonic3"  # Put your first variable label here
VARIABLE_LABEL_4 = "ultrasonic4"  # Put your second variable label here
VARIABLE_LABEL_5 = "ultrasonic5"
VARIABLE_LABEL_6 = "ultrasonic6"
VARIABLE_LABEL_7 = "ultrasonic7"
VARIABLE_LABEL_8 = "ultrasonic8"
VARIABLE_LABEL_9 = "position"

def build_payload(variable_1, variable_2, variable_3, variable_4, variable_5, variable_6, variable_7, variable_8, variable_9):
    # Creates two random values for sending data
    value_1 = random.randint(-10, 50)
    value_2 = random.randint(0, 85)
    value_3 = random.randint(2, 28)
    value_4 = random.randint(25, 27)
    value_5 = random.randint(10, 17)
    value_6 = random.randint(0, 20)
    value_7 = random.randint(8, 25)
    value_8 = random.randint(3, 30)

    # Creates a random gps coordinates
    lat = random.randrange(34, 36, 1) + \
        random.randrange(1, 1000, 1) / 1000.0
    lng = random.randrange(-83, -87, -1) + \
        random.randrange(1, 1000, 1) / 1000.0
 

    payload = {variable_1: value_1,
               variable_2: value_2,
               variable_3: value_3,
               variable_4: value_4,
               variable_5: value_5,
               variable_6: value_6,
               variable_7: value_7,
               variable_8: value_8,
               variable_9: {"value": 1, "context": {"lat": lat, "lng": lng}}}

    return payload


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "https://industrial.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def main():
    payload = build_payload(
        VARIABLE_LABEL_1, VARIABLE_LABEL_2, VARIABLE_LABEL_3, VARIABLE_LABEL_4, VARIABLE_LABEL_5, VARIABLE_LABEL_6, VARIABLE_LABEL_7, VARIABLE_LABEL_8, VARIABLE_LABEL_9)

    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")


if __name__ == '__main__':
    while (True):
        main()
        time.sleep(1)