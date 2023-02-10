from micropython import const
from machine import Pin, I2C

DS3231_ADDR = const(0x68)
DS3231_REG_SEC = b'\x00'
DS3231_REG_MIN = b'\x01'
DS3231_REG_HOUR = b'\x02'
DS3231_REG_WEEKDAY = b'\x03'
DS3231_REG_DAY = b'\x04'
DS3231_REG_MONTH = b'\x05'
DS3231_REG_YEAR = b'\x06'
DS3231_REG_A1SEC = b'\x07'
DS3231_REG_A1MIN = b'\x08'
DS3231_REG_A1HOUR = b'\x09'
DS3231_REG_A1DAY = b'\x0A'
DS3231_REG_A2MIN = b'\x0B'
DS3231_REG_A2HOUR = b'\x0C'
DS3231_REG_A2DAY = b'\x0D'
DS3231_REG_CTRL = b'\x0E'
DS3231_REG_STA = b'\x0F'
DS3231_REG_OFF = b'\x10'
DS3231_REG_TEMPM = b'\x11'
DS3231_REG_TEMPL = b'\x12'


class DS3231(object):
    def __init__(self, gpio_scl=5, gpio_sda=4, freq=100000, i2c=None):
        # 初始化i2c总线，可以外部传入也可以指定管脚在内部创建
    	self.i2c = i2c or I2C(scl=Pin(gpio_scl), sda=Pin(gpio_sda), freq=freq)

    def Date(self, dat=[]):
        '''读取或设置当前日期'''
        if dat == []:
            t = []
            t.append(str(self.year()))
            t.append(str(self.month()))
            t.append(str(self.day()))
            return t
        else:
            self.year(dat[0])
            self.month(dat[1])
            self.day(dat[2])

    def Time(self, dat=[]):
        '''读取或设置当前时间'''
        if not dat:
            t = []
            t.append(str(self.hour()))
            t.append(str(self.min()))
            t.append(str(self.sec()))
            return t
        else:
            self.hour(dat[0])
            self.min(dat[1])
            self.sec(dat[2])

    def DateTime(self, dat=[]):
        '''读取或设置当前日期与时间'''
        if dat == []:
            return self.Date() + self.Time()
        else:
            self.year(dat[0])
            self.month(dat[1])
            self.day(dat[2])
            self.hour(dat[3])
            self.min(dat[4])
            self.sec(dat[5])

    def _set_reg(self, reg, dat, trans_dec=True):
        '''写寄存器'''
        # 转换成寄存器需要的大小端分离格式
        dat = (int(dat / 10) << 4) + (dat % 10) if trans_dec else dat
        # 待发送数据：寄存器地址 + 设定值
        buf = bytearray(2)
        buf[0] = reg[0]
        buf[1] = dat
        self.i2c.writeto(DS3231_ADDR, buf)

    def _get_reg(self, reg, trans_dec=True):
        '''读寄存器'''
        # 指定待读取寄存器地址
        self.i2c.writeto(DS3231_ADDR, reg)
        # 读取1位数据
        t = self.i2c.readfrom(DS3231_ADDR, 1)[0]
        if trans_dec:  # 将大小端分离的格式数据转换为正常十进制
            return (t >> 4) * 10 + (t % 16)
        else:
            return t

    def sec(self, sec=''):
        if sec == '':
            return self._get_reg(DS3231_REG_SEC)
        else:
            self._set_reg(DS3231_REG_SEC, sec)

    def min(self, min=''):
        if min == '':
            return self._get_reg(DS3231_REG_MIN)
        else:
            self._set_reg(DS3231_REG_MIN, min)

    def hour(self, hour=''):
        if hour == '':
            return self._get_reg(DS3231_REG_HOUR)
        else:
            self._set_reg(DS3231_REG_HOUR, hour)

    def day(self, day=''):
        if day == '':
            return self._get_reg(DS3231_REG_DAY)
        else:
            self._set_reg(DS3231_REG_DAY, day)

    def month(self, month=''):
        if month == '':
            return self._get_reg(DS3231_REG_MONTH)
        else:
            self._set_reg(DS3231_REG_MONTH, month)

    def year(self, year=''):
        if year == '':
            return self._get_reg(DS3231_REG_YEAR)
        else:
            self._set_reg(DS3231_REG_YEAR, year)

    def Temperature(self):
        '''获取温度
        # t1是高8位，本来要左移两位的，因为温度分辨率还得除4，相当于不用移位了。
        # t2是低2位，但放置在了12H的最高位置上，所以需要右移6位（除以64），再加上分辨率因素（除4），所以t2/256就是实际值了。
        '''
        t1 = self._get_reg(DS3231_REG_TEMPM, trans_dec=False)
        t2 = self._get_reg(DS3231_REG_TEMPL, trans_dec=False)
        if t1 > 0x7F:  # 11H最高位为1代表负数
            return t1 - t2 / 256 - 256   # 补码简化算法，得数-256
        else:
            return t1 + t2 / 256