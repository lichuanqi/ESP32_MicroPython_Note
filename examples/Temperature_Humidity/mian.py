"""
通过温湿度传感器获取环境温度和湿度信息
MQTT发布消息
在OLED屏显示温湿度数据及消息发布状态
"""

import network
import time
from machine import Pin,I2C,Timer
import dht
import ujson
from simple import MQTTClient
from ssd1306 import SSD1306_I2C

# 参数
WIFI_NAME = '601'
WIFI_PWD = '1024601666'

MQTT_CLIENT_ID = 'ESP32_0001'
MQTT_BROKER = '192.168.31.99'
MQTT_PORT = '1883'
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_TOPIC = 'massage/environment'

# 初始化蓝色板载灯
LED_BLUE=Pin(2, Pin.OUT) #初始化WIFI指示灯

# 初始化DTH22
DHT = dht.DHT22(Pin(15))
time.sleep(1)

# 初始化oled屏
# i2c = I2C(sda=Pin(13), scl=Pin(12))
# oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)


def WIFI_Connect():
    """WIFI连接函数
    
    蓝灯闪烁-正在尝试连接
    蓝灯常量-连接成功
    蓝灯常闭-连接超时
    """
    wlan = network.WLAN(network.STA_IF) #STA模式
    wlan.active(True)                   #激活接口
    start_time=time.time()              #记录时间做超时判断

    if not wlan.isconnected():
        print('connecting to network...')
        # wlan.connect('cpst', 'cpstzykj')
        wlan.connect(WIFI_NAME, WIFI_PWD)

        while not wlan.isconnected():

            #LED闪烁提示
            LED_BLUE.value(1)
            time.sleep_ms(300)
            LED_BLUE.value(0)
            time.sleep_ms(300)

            #超时判断,10秒没连接成功判定为超时
            if time.time()-start_time > 10:
                print('WIFI Connected Timeout!')
                break

    if wlan.isconnected():
        LED_BLUE.value(0)
        print('WIFI Connected:', wlan.ifconfig())


def MQTT_connect():
    """连接mqt"""
    global mqttclient
    
    mqttclient = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT)
    mqttclient.connect()
    print('MQTT connected')


def publish_temp(tim):
    # 读取温湿度数据
    DHT.measure()
    temp, hum = DHT.temperature(), DHT.humidity()
    
    # 像主题发送数据
    message = ujson.dumps({
        "temp": temp,
        "hum": hum,
    })
    try:
        mqttclient.publish(MQTT_TOPIC, message)
        publish_status = 'True'
        print('publish success')
        
        # 亮灯1s
        LED_BLUE.value(1)
        time.sleep(1)
        LED_BLUE.value(0)
    except:
        publish_status = 'False'
        print('publish failed')

    # 屏幕显示温湿度及发送状态
    # oleDHT.fill(0)
    # oleDHT.text('temp: ' + str(temp), 0, 0)
    # oleDHT.text('humidity:' + str(hum), 0, 20)
    # oleDHT.text('Published:' + str(publish_status), 0, 38)
    # oleDHT.show()


if __name__ == '__main__':
    # 连接wifi
    WIFI_Connect()
    
    # 连接MQTT
    MQTT_connect()

    # 定时器
    tim = Timer(-1)
    publish_temp(tim)
    tim.init(period=5000, mode=Timer.PERIODIC,callback=publish_temp)