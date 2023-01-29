"""
4位数码管显示数字
"""

import machine
import time


led1 = machine.Pin(5, machine.Pin.OUT)
led2 = machine.Pin(18, machine.Pin.OUT)
led3 = machine.Pin(19, machine.Pin.OUT)
led4 = machine.Pin(21, machine.Pin.OUT)

number_led_list = [led1, led2, led3, led4]


a = machine.Pin(13, machine.Pin.OUT)
b = machine.Pin(12, machine.Pin.OUT)
c = machine.Pin(14, machine.Pin.OUT)
d = machine.Pin(27, machine.Pin.OUT)
e = machine.Pin(26, machine.Pin.OUT)
f = machine.Pin(25, machine.Pin.OUT)
g = machine.Pin(33, machine.Pin.OUT)
h = machine.Pin(32, machine.Pin.OUT)

# 将对应的引脚对象存储到列表
led_list = [a, b, c, d, e, f, g, h]

number_dict = {
    0: "11111100",
    1: "01100000",
    2: "11011010",
    3: "11110010",
    4: "01100110",
    5: "10110110",
    6: "10111110",
    7: "11100000",
    8: "11111110",
    9: "11110110",
}

def show_number(number):
    if number_dict.get(number):
        i = 0
        for num in number_dict.get(number):  # 此时就是对应的value，即类似的"01110111"
            if num == "1":
                led_list[i].value(0)
            else:
                led_list[i].value(1)
            i += 1
            
def led_light_on(i):
    # 全部设置为0
    for led in number_led_list:
        led.value(0)
        
    number_led_list[i].value(1)

def show_4_number(number):
    if 0 <= number <= 9999:
        i = 0
        for num in "%04d" % number:
            print(num)
            show_number(int(num))
            led_light_on(i)
            time.sleep_ms(5)
            i += 1

for i in range(1234, 10000):
    for j in range(10):
        show_4_number(i)