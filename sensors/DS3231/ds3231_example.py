import json
import urequests
from machine import Pin,I2C,Time

from ds3231 import DS3231
from ...utils.urequest import get
from ...utils.ssd1306 import SSD1306_I2C


def reset_time(ds:DS3231):
    """网络校时
    
    Params
        ds: DS3231模块
    """
    system_time = ds.DateTime()
    print('system time: %s'%system_time)

    url = 'http://quan.suning.com/getSysTime.do'
    res = get(url).text
    
    j=json.loads(res)
    t2_date = j['sysTime2'].split()[0] # 日期
    t2_time = j['sysTime2'].split()[1] # 时间
    print('internet time: %s %s'%(t2_date, t2_time))

    # 设置初始日期年、月、日
    ds.Date([int(x) for x in t2_date[2:].split('-')])
    # 设置初始时间时、分、秒
    ds.Time([int(x) for x in t2_time.split(':')])


# 初始化DS3231模块
ds = DS3231(gpio_scl=5, gpio_sda=4)
reset_time(ds)

# 初始化显示模块
i2c = I2C(sda=Pin(13), scl=Pin(14))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

# 获取日期、时间
ds.DateTime()
# 获取当前温度
ds.Temperature()

# 设置日期时间（注意用短年份）
ds.DateTime([21, 8, 18, 12, 0, 0])  
# 仅设置时间
ds.Time([12, 1, 0])