'''
连接wifi
实现连接路由器，将IP地址等相关信息通过OLED显示（只支持2.4G网络）。
'''
import network,time
from machine import I2C,Pin
from ssd1306 import SSD1306_I2C


# 参数
WIFI_NAME = '601'
WIFI_PWD = '1024601666'

#初始化相关模块
i2c = I2C(sda=Pin(13), scl=Pin(14))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)


def WIFI_Connect():
    """WIFI连接函数
    蓝灯闪烁-正在尝试连接
    蓝灯常量-连接成功
    蓝灯常闭-连接超时
    """

    WIFI_LED=Pin(2, Pin.OUT) #初始化WIFI指示灯

    wlan = network.WLAN(network.STA_IF) #STA模式
    wlan.active(True)                   #激活接口
    start_time=time.time()              #记录时间做超时判断

    if not wlan.isconnected():
        wlan.connect(WIFI_NAME, WIFI_PWD)
        print('connecting to network...')

        while not wlan.isconnected():
            # LED闪烁提示
            WIFI_LED.value(1)
            time.sleep_ms(300)
            WIFI_LED.value(0)
            time.sleep_ms(300)

            # 超时判断,15秒没连接成功判定为超时
            if time.time()-start_time > 15 :
                print('WIFI Connected Timeout!')
                break

    if wlan.isconnected():
        # 打印网络信息
        print('network information:', wlan.ifconfig())
        
        # LED点亮
        WIFI_LED.value(1)

        # OLED数据显示
        oled.fill(0)   #清屏背景黑色
        oled.text('IP/Subnet/GW:',0,0)
        oled.text(wlan.ifconfig()[0], 0, 20)
        oled.text(wlan.ifconfig()[1],0,38)
        oled.text(wlan.ifconfig()[2],0,56)
        oled.show()


if __name__ == '__main__':
    WIFI_Connect()
