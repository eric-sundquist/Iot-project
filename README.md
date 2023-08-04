# Van Climate Monitoring System with IoT

---
**Table of Contents**

[TOC]


---


## Van Climate Monitoring System with IoT
_By Eric Sundqvist - es225kz@student.lnu.se_
_LNU username: es225kz_



This project aims to create an IoT-based system for monitoring the indoor climate of a van, or other house forms, using a DHT22 temperature and humidity sensor, and a Raspberry Pi Pico W. The data collected will be visualized on the Adafruit IO platform, allowing real-time and historical tracking of temperature and humidity levels. This system will enhance comfort in the van while providing practical experience with IoT devices.

An estimation of time to complete the project is 5-15 hours depending on previous knowledge.

### Objective

I have been living in a van all year around for sevral years. Living in a little box of metal comes with its advantages and disadvantages. One potential issue can be humidity. With a tiny space the relative humidty can is quickly affected by the personen living in it. For example if you bring in wet clothes or forget to start the fan when you are cooking you will quickly notice this. Since there is often a steep temperature gradient between the outside metal and the inside of the van, due to limited space and insulation, condensation can often become a problem. This is not nice inside the van and can also often lead to mold issues in the long term. Hence it is important to continuesly check the relative humidity so that you know when you need to try to lower it by for example by running your ventilation and heater.

Living in a van for several years has given me firsthand experience of the advantages and challenges associated with this lifestyle. One significant challenge I encountered was maintaining optimal humidity levels inside the confined space. This issue often leads to condensation and, in the long term, potential mold problems. To address this, I decided to undertake a project that focuses on developing a device for monitoring both relative humidity and temperature inside the van.

The purpose of this device is to provide real-time monitoring of humidity and temperature within the van. By continuously measuring these parameters, it allows for proactive control of humidity levels, preventing condensation issues, and creating a comfortable living environment. Additionally, considering the substantial temperature gradient between the van's metal exterior and its interior, temperature measurement plays a crucial role in understanding how temperature differentials affect humidity levels. By incorporating temperature measurement alongside humidity monitoring, the device will offer a solution for monitoring optimal conditions inside the van.

Through this project, I anticipate gaining valuable insights into the dynamics of humidity and temperature control within a van. Analyzing the collected data will enable me to identify patterns, correlations, and potential triggers for humidity fluctuations. These insights will empower me to optimize living conditions by making informed decisions regarding ventilation and heating strategies, thus minimizing condensation and fostering a healthier environment.

### Material

| Image    | IoT Thing                            | Purpose                                                                                                                                                                                    | Price                             |
| --- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------- |
|  ![Raspberry Pico W](https://m.media-amazon.com/images/I/51hBdL4tAVL._SY180_.jpg)   | Raspberry Pico W (pre-soldered pins) | Versatile microcontroller board suitable for IoT projects. It features a dual-core RP2040 chip, programmable input/output pins, and wifi. Programable with micropython                     | EUR 20 from Amazon.fr             |
|   ![DHT22 sensor](https://m.media-amazon.com/images/I/41FrMzaTAKL._SY180_.jpg)  |              DHT22                        |                                           Temperature and Humidity sensor. Reads relative humidity from 0-100% with a 2-5% accuracy and temperature, -40-80C, with a +-0.5C accuracy. | EUR 13  from Amazon.fr            |
| ![Breadboard](https://m.media-amazon.com/images/I/51VXpV8Y7WL._SY180_.jpg)    | Breadboard                           | Makes it easier to connect sensors to the microcontroller.                                                                                                                                 | EUR 4 from Amazon.fr              |
|   ![dupont cables](https://m.media-amazon.com/images/I/51iARJefS3L._SY180_.jpg)  | Dupont/jumper wires                  | Connects the sensor to the microcontroller through with the help of the breadboard                                                                                                         | EUR 7 from Amazon.fr (120 pieces) |
|   ![micro usb cable](https://m.media-amazon.com/images/I/614H6oGzuPL._AC_UL800_FMwebp_QL65_.jpg)  | Micro USB-cable                      | For communicating/uploading code to the microcontroller and provides it with power.                                                                                                        |  In my case included with the microcontroller. Estimated cost EUR 4. Can be bought from most home electronic stores.                                  |


### Computer setup

I choose to use [VSCode](https://code.visualstudio.com/download) as the IDE. You need to have a recent version of VScode for it to work with the plugins. To communicate and upload code to the Pico W you use the [Pico-W-GO](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go) vscode extension. Before you can start programming the microcontroller you need to flash the firmware of the Rasberry Pico W. To do this you follow these [instructions](https://projects.raspberrypi.org/en/projects/get-started-pico-w/1).

### Putting everything together
Follow the following instructions for connecting the electronics. Note that this setup is for development and it might not be suitable to use in a production environment.

Connect the Pico W to the breadboard and route the male-male dupont wires like this circuit diagram. 
![Circut diagram](https://images2.imgbox.com/20/cc/8QqWNXI1_o.jpg)

Please refere two the Pico W pinout table here to find the right pins:
![Pico W pinout](https://www.raspberrypi-spy.co.uk/wp-content/uploads/2022/11/raspberry_pi_pico_w_pinout.png)

Connect the micro usb cable. The finishing result should look something like this.
![Example 1](https://images2.imgbox.com/97/82/W3b7Nm7u_o.jpg)
![Example 2](https://images2.imgbox.com/71/65/UhBKcvma_o.jpg)

**Note on resistors**
Normaly you would use an external pullup resistor with for the temperature sensor. However the Pico W has these internaly built in and it can be used/activated programaticly. 



### Platform

I have chosen the [Adafruit IO](https://io.adafruit.com/) platform for collecting and visualizing data for my project.

The Adafruit IO platform offers a cloud-based solution for IoT projects, allowing for seamless data collection and visualization. I chose to use this platform because of the following reasons:
- User-friendly interface and various functionalities to manage and analyze the collected data
- Generous free tier
- Easy setup and use

In terms of scalability, Adafruit IO offers different subscription plans beyond the free tier. If I decide to scale up my project in the future, I can explore the paid subscription options provided by the platform. Altough this is highly unlikely for a project like this.

### The code

**File: boot.py**
This script runs on boot up and tries to connect to wifi.
```python=
import network, utime

SSID = "WIFI_NAME"
SSID_PASSWORD = "WIFI_PASSWORD"


def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, SSID_PASSWORD)
        while not sta_if.isconnected():
            print("Attempting to connect....")
            utime.sleep(1)
    print('Connected! Network config:', sta_if.ifconfig())
    
print("Connecting to your wifi...")
do_connect()
```

**File: main.py**
This script runs after boot up. It tries to connect to the Adafruit MQTT broker. Then it collects the sensor data and sends it to the Adafruit broker every 5 seconds. It also setups the intergrated led lamp of the pico W so that it can be toggled via Adafruit IO.
```python=
import time
import ubinascii
from umqttsimple import MQTTClient
import machine
import dht #temperature sensor library
import json

# Details for connecting to Adafruit IO
CLIENT_ID = ubinascii.hexlify(machine.unique_id()) 
MQTT_BROKER = "io.adafruit.com"   
PORT = 1883
ADAFRUIT_USERNAME = "username"
ADAFRUIT_PASSWORD = "password" 
SUBSCRIBE_LED = b"path_to_led"
PUBLISH_TEMP_HUMI = b"path_to_temp_and_humidity"

Pin = machine.Pin
led = Pin("LED",Pin.OUT) # assigning the led pin to a varaiable
dht_sensor = dht.DHT22(Pin(14, Pin.IN, Pin.PULL_UP)) #setup the sensor reading pin with the DHT22 library and use pullup-resistor

# Publish MQTT messages after every set timeout
last_publish = time.time()  # last_publish variable will hold the last time a message was sent.
publish_interval = 5 #5 seconds --> this means a new message will be sent every 5 seconds

# Reads the temperature data and returns a json string with the data
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
```

>The code aboce uses a library for the setting up and connecting to a mqtt client. To use this library create a file in root of the project named umqttsimple.py and copy and paste the source code from [here](https://github.com/iot-lnu/applied-iot/blob/master/1DV027/mqtt-pico-w/umqttsimple.py)


### Transmitting the data / connectivity
The data is sent from the Pico W every 5 seconds. The data is formated into json

To transmit the data from my device to the Adafruit IO endpoint, I utilize the MQTT (Message Queuing Telemetry Transport) protocol over a Wi-Fi connection. Here is a breakdown of the steps involved in getting the data to the endpoint:

Data Format: The data is formatted in JSON (JavaScript Object Notation) format. JSON provides a lightweight and easily parseable structure for representing the data being transmitted.

Wireless Protocol: The device communicates over Wi-Fi to establish a network connection. Wi-Fi offers a reliable and widely available wireless communication method for connecting IoT devices to the internet.

MQTT Protocol: MQTT is used as the transport protocol for publishing the data to the Adafruit IO endpoint. MQTT is a lightweight messaging protocol designed for efficient communication between IoT devices and servers.

Publish Frequency: The data is sent every 5 seconds. This frequency can be adjusted based on the specific requirements of the project and the desired rate of data transmission.

Connection and Authentication: The device establishes a connection with the Adafruit IO MQTT broker by providing username and password. 

Publish to Adafruit IO: Once connected, the device publishes the data in JSON format to the corresponding topic on the Adafruit IO MQTT broker. The topic represents the destination or category to which the data belongs.


### Presenting the data

The presentation part of my project involves building a dashboard on the Adafruit IO platform to visualize the collected data. Using the Adafruit IO platform, I have created a dashboard that displays the temperature and humidity data in two graphs. Adafruit IO provides many ways to customize the layout and design, enabling me to create an intuitive and user-friendly interface for data visualization. 

The data collected and published to the Adafruit IO platform is preserved in the database for a configurable period. The specific duration of data preservation depends on the subscription plan chosen. In the free tier, Adafruit IO retains the data for 30 days.

The frequency at which data is saved in the database is determined by the publish rate set in the device code. In this project, the data is published and saved every 5 seconds. However, the data saving frequency can be adjusted based on project requirements and the desired granularity of data collection.

Here is an example visual representation of the dashboard:

![image alt](https://images2.imgbox.com/df/d3/PY0X7d43_o.png)
 


### Finalizing the design
<iframe width="560" height="315" src="https://www.youtube.com/embed/gYxOSwHgKmQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe> 
[video](https://www.youtube.com/watch?v=gYxOSwHgKmQ)

The video above showcases the result of my project. It is still very much a development protoype but it still works in a satisfactory way. I choose to keep the project simple and using adafruit IO as mqtt broker and for presenting the data was nice and very simple. 

In the future it would be interesting to add more sensors such as a carbon monoxide/dioxid sensor and build an app for my android phone to display the values. It would also be nice to add a display so that you can instantly see the measurments without needing a internet connection. When I finalize the design I will make an enclosure for the device and do without the breadboard to alow for a smaller and neater design. 

---
