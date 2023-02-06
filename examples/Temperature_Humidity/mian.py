"""
通过温湿度传感器获取环境温度和湿度信息
MQTT发布消息
在OLED屏显示温湿度数据及消息发布状态
"""
import time
import ujson
import network
from machine import Pin,SoftI2C,ADC,Timer

import dht
from simple import MQTTClient
from ssd1306 import SSD1306_I2C
from bh1750 import BH1750

# 参数
WIFI_NAME = 'WiWide-BurgerKing'
WIFI_PWD = 'qwer1234'

MQTT_CLIENT_ID = 'ESP32_0002'
MQTT_BROKER = '192.168.35.221'
MQTT_PORT = '1883'
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_TOPIC = 'massage/environment'

# 板载蓝灯
LED_BLUE=Pin(2, Pin.OUT)

# OLED模块
i2c = SoftI2C(sda=Pin(19), scl=Pin(21))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)
oled.fill(0)
oled.text('init over', 0, 0)
oled.show()

# BH1750模块
i2c_bh1750 = SoftI2C(scl=Pin(23), sda=Pin(22), freq=100000)
bh1750 = BH1750(i2c_bh1750)
# light = bh1750.luminance(mode=BH1750.ONCE_HIRES_1)
# print('light: %s'%(light))

# DHT22模块 
d = dht.DHT22(Pin(15))
time.sleep(1)
d.measure()
temp, hum = d.temperature(), d.humidity()
print('temp: %s, hum: %s'%(temp, hum))


def Connect_WIFI():
    """WIFI连接函数
    
    蓝灯闪烁-正在尝试连接
    蓝灯常量-连接成功
    蓝灯常闭-连接超时
    """
    wlan = network.WLAN(network.STA_IF) #STA模式
    wlan.active(True)                   #激活接口
    start_time=time.time()              #记录时间做超时判断

    if not wlan.isconnected():
        wlan.connect(WIFI_NAME, WIFI_PWD)
        oled.text('Connecting Wifi', 0, 15)
        oled.show()

        while not wlan.isconnected():
            #LED闪烁提示
            LED_BLUE.value(1)
            time.sleep_ms(300)
            LED_BLUE.value(0)
            time.sleep_ms(300)

            #超时判断,10秒没连接成功判定为超时
            if time.time()-start_time > 10:
                oled.text('Timeout!', 0, 30)
                break

    if wlan.isconnected():
        LED_BLUE.value(0)
        oled.text('Success', 0, 30)
        oled.show()


def connect_MQTT():
    """连接mqt"""
    global mqttclient
    
    mqttclient = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT)
    mqttclient.connect()
    oled.text('MQTT connected', 0, 45)
    oled.show()


def measure_once(tim):    
    # 光强度数据
    light = bh1750.luminance(mode=BH1750.ONCE_HIRES_1)
    # 温湿度数据
    d.measure()
    temp, hum = d.temperature(), d.humidity()
    
    # 像主题发送数据
    message = ujson.dumps({
        "temp": temp,
        "hum": hum,
        "light": light,
    })
    try:
        mqttclient.publish(MQTT_TOPIC, message)
        state = 'success'
        
        # 亮灯1s
        LED_BLUE.value(1)
        time.sleep(1)
        LED_BLUE.value(0)
    except:
        state = 'failed'
    
    oled.fill(0)
    oled.text('Light: ' + str(light), 0, 0)
    oled.text('Temp: ' + str(temp), 0, 15)
    oled.text('Humi: ' + str(hum), 0, 30)
    oled.text('State: ' + state, 0, 45)
    oled.show()


if __name__ == '__main__':
    
    Connect_WIFI()
    connect_MQTT()

    # 定时器
    tim = Timer(-1)
    # measure_once(tim)
    tim.init(period=10000, mode=Timer.PERIODIC,callback=measure_once)