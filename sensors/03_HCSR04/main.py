'''
超声波传感器测距，并在OLED上显示。
'''
from machine import Pin,I2C,Timer
from ssd1306 import SSD1306_I2C
from hcsr04 import HCSR04

# OLED模块
i2c = I2C(sda=Pin(19), scl=Pin(21))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

# HCSR04模块
HC=HCSR04(trig=Pin(32,Pin.OUT),echo=Pin(33,Pin.IN))

#中断回调函数
def fun(tim):

    # 清屏,背景黑色
    oled.fill(0) 
    oled.text('Distance test:', 0, 0)
    
    # 测量距离
    Distance = HC.getDistance()
    print(str(Distance)+' CM')

    # OLED显示距离
    oled.text(str(Distance) + ' CM', 0, 20)
    oled.show()


#开启RTOS定时器
tim = Timer(-1)
tim.init(period=1000, mode=Timer.PERIODIC, callback=fun) #周期1s