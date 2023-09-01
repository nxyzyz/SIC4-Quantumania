import RPi.GPIO as GPIO
import time
import requests

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# set GPIO Pins for the first ultrasonic sensor
GPIO_TRIGGER_1 = 21
GPIO_ECHO_1 = 20

# set GPIO Pins for the second ultrasonic sensor
GPIO_TRIGGER_2 = 23
GPIO_ECHO_2 = 24

GPIO_GREEN = 25
GPIO_YELLOW = 26
GPIO_GREEN1 = 6
GPIO_YELLOW1 =17

# set GPIO direction (IN / OUT) for the first ultrasonic sensor
GPIO.setup(GPIO_TRIGGER_1, GPIO.OUT)
GPIO.setup(GPIO_ECHO_1, GPIO.IN)
GPIO.setup(GPIO_GREEN, GPIO.OUT)
GPIO.setup(GPIO_YELLOW, GPIO.OUT)
GPIO.setup(GPIO_GREEN1, GPIO.OUT)
GPIO.setup(GPIO_YELLOW1, GPIO.OUT)

# set GPIO direction (IN / OUT) for the second ultrasonic sensor
GPIO.setup(GPIO_TRIGGER_2, GPIO.OUT)
GPIO.setup(GPIO_ECHO_2, GPIO.IN)

def distance(trigger_pin, echo_pin):
    GPIO.output(trigger_pin, True)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, False)
    
    start_time = time.time()
    stop_time = time.time()
    
    while GPIO.input(echo_pin) == 0:
        start_time = time.time()
    
    while GPIO.input(echo_pin) == 1:
        stop_time = time.time()
    
    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2
    return distance

TOKEN = "BBFF-uVoTmcQMzeatMopL6gYzNqKBNz6k3O"
DEVICE_LABEL = "qu4ntumania"
VARIABLE_LABEL_1 = "potato_snack"
VARIABLE_LABEL_2 = "chocolate_snack"

def jumlah_barang():
    distance_1 = distance(GPIO_TRIGGER_1, GPIO_ECHO_1)
    if distance_1 <= 5:
        jumlah_barang = 5
    elif distance_1 <= 10:
        jumlah_barang = 4
    elif distance_1 <= 15:
        jumlah_barang = 3
    elif distance_1 <= 20:
        jumlah_barang = 2
    elif distance_1 <= 25:
        jumlah_barang = 1
    else:
        jumlah_barang = 0

    return jumlah_barang

def jumlah_barang_2():
    distance_2 = distance(GPIO_TRIGGER_2, GPIO_ECHO_2)
    if distance_2 <= 5:
        jumlah_barang_2 = 5
    elif distance_2 <= 10:
        jumlah_barang_2 = 4
    elif distance_2 <= 15:
        jumlah_barang_2 = 3
    elif distance_2 <= 20:
        jumlah_barang_2 = 2
    elif distance_2 <= 25:
        jumlah_barang_2 = 1
    else:
        jumlah_barang_2 = 0
    
    return jumlah_barang_2

jumlah = 0
jumlah2 = 0
    
def build_payload(variable_1, variable_2):
    global jumlah, jumlah2
    jumlah = jumlah_barang()
    jumlah2 = jumlah_barang_2()

    value_1 = jumlah
    value_2 = jumlah2
    
    payload = {
        variable_1: value_1,
        variable_2: value_2,
    }
    
    return payload

def post_request(payload):
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True

def main():
    payload = build_payload(VARIABLE_LABEL_1, VARIABLE_LABEL_2)
    print("[INFO] Attempting to send data")
    post_request(payload)
    print("[INFO] Finished")

while True:
    distance_1 = round(distance(GPIO_TRIGGER_1, GPIO_ECHO_1))
    distance_2 = round(distance(GPIO_TRIGGER_2, GPIO_ECHO_2))
    
    main()
    if jumlah >=3:
        GPIO.output(GPIO_GREEN, GPIO.HIGH)
        GPIO.output(GPIO_YELLOW, GPIO.LOW)
    elif jumlah <=2:
        GPIO.output(GPIO_GREEN, GPIO.LOW)
        GPIO.output(GPIO_YELLOW, GPIO.HIGH)
        
    if jumlah2 >=3:
        GPIO.output(GPIO_GREEN1, GPIO.HIGH)
        GPIO.output(GPIO_YELLOW1, GPIO.LOW)
    elif jumlah2 <=2:
        GPIO.output(GPIO_GREEN1, GPIO.LOW)
        GPIO.output(GPIO_YELLOW1, GPIO.HIGH)
    print("Jarak:", distance_1, "cm", "Item Count:", jumlah,"(ULTRASONIC 1)")
    print("Jarak:", distance_2, "cm", "Item Count:", jumlah2,"(ULTRASONIC 2)")
    time.sleep(1)