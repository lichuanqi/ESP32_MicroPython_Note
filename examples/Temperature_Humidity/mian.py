"""
MicroPython IoT Weather Station Example for Wokwi.com

To view the data:

1. Go to http://www.hivemq.com/demos/websocket-client/
2. Click "Connect"
3. Under Subscriptions, click "Add New Topic Subscription"
4. In the Topic field, type "wokwi-weather" then click "Subscribe"

Now click on the DHT22 sensor in the simulation,
change the temperature/humidity, and you should see
the message appear on the MQTT Broker, in the "Messages" pane.

Copyright (C) 2022, Uri Shaked

https://wokwi.com/arduino/projects/322577683855704658
"""

import network
import time
from machine import Pin,I2C
import dht
import ujson
from umqtt.simple import MQTTClient
from ssd1306 import SSD1306_I2C


# MQTT Server Parameters
MQTT_CLIENT_ID = "micropython-weather-demo"
MQTT_BROKER        = "broker.mqttdashboard.com"
MQTT_USER            = ""
MQTT_PASSWORD    = ""
MQTT_TOPIC         = "wokwi-weather"

# 初始化温湿度传感器
sensor = dht.DHT22(Pin(15))

#初始化相关模块
i2c = I2C(sda=Pin(13), scl=Pin(12))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

# 连接wifi
print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.1)
print(" Connected!")

# 连接MQTT服务器
print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, 
                                        user=MQTT_USER, password=MQTT_PASSWORD)
client.connect()
print("Connected!")

prev_weather = ""
while True:
    print("Measuring weather conditions... ", end="")
    sensor.measure() 
    message = ujson.dumps({
        "temp": sensor.temperature(),
        "humidity": sensor.humidity(),
    })
    
    # 屏幕显示温湿度
    oled.fill(0)
    oled.text('temp: ' + str(sensor.temperature()), 0, 0)
    oled.text('humidity:' + str(sensor.humidity()), 0, 20)

    # 如果与上次数值则不发送
    if message != prev_weather:
        print("Updated!")
        print("Reporting to MQTT topic {}: {}".format(MQTT_TOPIC, message))
        client.publish(MQTT_TOPIC, message)
        prev_weather = message
        publish_status = 'True'
    else:
        print("No change")
        publish_status = 'False'

    # 显示发送状态
    oled.text('Published:' + str(publish_status), 0, 38)
    oled.show()

    time.sleep(1)