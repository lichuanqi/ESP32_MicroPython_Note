'''点亮LED蓝灯'''

from machine import Pin 

# 构建led对象，GPIO2,输出
led=Pin(2,Pin.OUT) 
# 点亮LED，也可以使用led.on()
led.value(1) 
