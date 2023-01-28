'''
读取温湿度传感器DHT22数据
'''
from machine import Pin,I2C,Timer
# from ssd1306 import SSD1306_I2C
import dht,time

# 初始化DTH22
d = dht.DHT22(Pin(15)) #传感器连接到引脚15
time.sleep(1)   #首次启动停顿1秒让传感器稳定

# 初始化显示模块
# i2c = I2C(sda=Pin(13), scl=Pin(14))
# oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)


def get_temp_hum():
    """获取温湿度数据"""
    d.measure()
    temp, hum = d.temperature(), d.humidity()
    
    return temp, hum


def print_temp_hum(tim):
    """终端输出温湿度数据"""
    temp, hum = get_temp_hum()
    print('temp: %s, hum: %s'%(temp,hum))

# def oled_temp_hum():
#     """OLED屏幕中显示温湿度数据"""
#     temp, hum = get_temp_hum()
    
    # oled.fill(0) #清屏背景黑色
    # oled.text('01Studio', 0, 0)
    # oled.text('DHT11 test:',0,15)
    # oled.text(str(d.temperature() )+' C',0,40)   #温度显示
    # oled.text(str(d.humidity())+' %',48,40)  #湿度显示
    # oled.show()


if __name__ == '__main__':

    # 开启RTOS定时器，编号为-1, 周期为2000ms
    tim = Timer(-1)
    print_temp_hum(tim)
    # tim.init(period=5000, mode=Timer.PERIODIC,callback=print_temp_hum)
