'''
控制舵机SG90

180度舵机：angle:-90至90 表示相应的角度
360连续旋转度舵机：angle:-90至90 旋转方向和速度值。

接线
红色-VCC
棕色-GND
橙色-信号线
'''
from machine import Pin, PWM
import time

S1 = PWM(Pin(13), freq=50, duty=0)


def Servo(servo, angle):
    S1.duty(int(((angle+90)*2/180+0.5)/20*1023))

#-90度
Servo(S1,0)
time.sleep(2)