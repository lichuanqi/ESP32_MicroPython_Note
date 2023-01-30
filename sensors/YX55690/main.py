"""
光敏传感器

主要部分是光敏电阻，它随着光强的变化而改变其电阻，
随着光强度的增加，光敏电阻的电阻将降低，因此输出电压降低。
光敏电阻传感器有两个LED指示灯。PWR-LED是电源指示灯。
DO-LED是数字输出指示灯，光弱时熄灭DO输出高电平；光强时灯亮DO输出低电平。
判定光强弱的临界值可以通过旋转中间蓝色元件上的十字螺丝调节。

引脚定义

引脚    功能
GND    电源地
VCC	   电源正（3.3V~5V）
AO	   模拟量输出
DO	   数字量输出


硬件连接

ESP32	光敏电阻模块
GND     GND
3V3     VCC
X23     AO
"""

import time
from machine import Pin,I2C,ADC,Timer

# 初始化模块
yx55690 = ADC(Pin(15))


def get_light_intensity():
    light = str(yx55690.read())
    print(light)


def get_light_intensity_n(n:int):
    for i in range(n):
        get_light_intensity()
        time.sleep(2)

if __name__ == '__main__':

    # 开启RTOS定时器，编号为-1, 周期为2000ms
    tim = Timer(-1)
    get_light_intensity_n(20)
    # tim.init(period=5000, mode=Timer.PERIODIC,callback=print_temp_hum)