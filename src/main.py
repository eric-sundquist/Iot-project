import time
import ubinascii
from umqttsimple import MQTTClient
import machine
import dht
import json

CLIENT_ID = ubinascii.hexlify(machine.unique_id()) 
MQTT_BROKER = "io.adafruit.com"   
PORT = 1883
ADAFRUIT_USERNAME = "ericsund"
ADAFRUIT_PASSWORD = "aio_tjEW843RgvstCMrWaURwWexgnZjz" 
SUBSCRIBE_LED = b"ericsund/feeds/led"
PUBLISH_TEMP_HUMI = b"ericsund/groups/picow-temp-humi/json"
Pin = machine.Pin
led = Pin("LED",Pin.OUT)
dht_sensor = dht.DHT22(Pin(14, Pin.IN, Pin.PULL_UP))

# Publish MQTT messages after every set timeout
last_publish = time.time()  # last_publish variable will hold the last time a message was sent.
publish_interval = 5 #5 seconds --> this means a new message will be sent every 5 seconds

def get_sensor_json_data():
    dht_sensor.measure()
    return json.dumps({
        "feeds": {
            "temp": dht_sensor.temperature(),
            "humi": dht_sensor.humidity()
        }
    })


# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
    print((topic, msg))
    if msg.decode() == "ON":
        led.value(1)
    else:
        led.value(0)


# if PicoW Failed to connect to MQTT broker. Reconnecting...'
def reset():
    print("Resetting...")
    time.sleep(5)
    machine.reset()

def main():
    print(f"Begin connection with MQTT Broker :: {MQTT_BROKER}")
    mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER, PORT, ADAFRUIT_USERNAME, ADAFRUIT_PASSWORD, keepalive=60)
    mqttClient.set_callback(sub_cb)
    mqttClient.connect()
    mqttClient.subscribe(SUBSCRIBE_LED)
    print(f"Connected to MQTT Broker :: {MQTT_BROKER}")
    while True:
            # Non-blocking wait for message
            mqttClient.check_msg()
            global last_publish
            if (time.time() - last_publish) >= publish_interval:
                mqttClient.publish(PUBLISH_TEMP_HUMI, get_sensor_json_data())
                last_publish = time.time()
                print("Sent sensor data...")
            time.sleep(1)


if __name__ == "__main__":
    while True:
        try:
            main()
        except OSError as e:
            print("Error: " + str(e))
            reset()