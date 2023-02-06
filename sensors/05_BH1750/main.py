import time
from machine import Pin,SoftI2C,ADC,Timer
from ssd1306 import SSD1306_I2C
from bh1750 import BH1750


# OLED模块
i2c = SoftI2C(sda=Pin(19), scl=Pin(21))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)
oled.fill(0)
oled.text('init over', 0, 0)
oled.show()

# BH1750模块
i2c_bh1750 = SoftI2C(scl=Pin(4), sda=Pin(2), freq=100000)
bh1750 = BH1750(i2c_bh1750)
bh1750_data = bh1750.luminance(mode=BH1750.ONCE_HIRES_1)
print(bh1750_data)

oled.fill(0)
oled.text('bh1750: ' + str(bh1750_data) + 'Lux', 0, 0)
oled.show()