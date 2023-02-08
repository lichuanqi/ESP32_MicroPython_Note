"""
SHT3X系列是由瑞士Sensirion生产的高精度温湿度传感器，
也是Sensirion公司目前主打的温湿度传感器系列。
现在网上常见的相关资料调试的基本上以SHT30为主，
SHT31则较少。当然，现在官网上还有了更高级的SHT35系列。

SHT31-DIS传感器允许宽电压输入，支持2.4V~5.5V（官网标注的实际SHT31系列最低支持电压为2.15V）。
采用IIC总线通信，最高可达1MHz的通信速度。
并根据ADDR引脚的接法，提供两个可选的地址。
传感器的精度为2%RH和0.3℃。传感器最大工作范围-40-125℃，0-100%RH。
原装芯片有8个引脚。

1.SDA :IIC数据线引脚
2.ADDR :地址引脚，可连接VSS或VDD，分别会有不同的地址。不能浮空。
3.ALERT :报警引脚，如果使用，建议接到单片机的外部中断。不用的话建议浮空。
4.SCL :IIC时钟线引脚
5. VDD :电压输入引脚
6.nRESET :复位引脚，低电平有效。如果不用，建议接到VDD。
7.R :没有电气作用的“没卵用“”引脚，连接到VSS
8. VSS :接地


"""

from machine import Pin, SoftI2C
import sht31


i2c = SoftI2C(scl=Pin(5), sda=Pin(18), freq =400000)
sensor = sht31.SHT31(i2c, addr=0x44)
temp, humi = sensor.get_temp_humi()
print('temp: %s, humi: %s'%(temp, humi))