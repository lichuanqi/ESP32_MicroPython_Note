"""
HCSR04 超声波传感器

介绍
HC-SR04超声波距离传感器的核心是两个超声波传感器。
一个用作发射器，将电信号转换为40 KHz超声波脉冲。接收器监听发射的脉冲。
如果接收到它们，它将产生一个输出脉冲，其宽度可用于确定脉冲传播的距离。

参数
Operating Voltage工作电压	直流5V
Operating Current工作电流	15毫安
Operating Frequency运行频率	40K赫兹
Max Range最大范围	4m
Min Range最小范围	2厘米
Ranging Accuracy测距精度	3毫米
Measuring Angle测量角度	15度
Trigger Input Signal触发输入信号	10µS TTL脉冲
Dimension尺寸	45 x 20 x 15毫米
"""
from time import sleep_us,ticks_us,sleep


class HCSR04():
    def __init__(self,trig,echo):
        self.trig=trig
        self.echo=echo

    def getDistance(self):
        distance=0
        self.trig.value(1)
        sleep_us(20)
        self.trig.value(0)
        while self.echo.value() == 0:
            pass
        if self.echo.value() == 1:
            ts=ticks_us()                   #开始时间
            while self.echo.value() == 1:   #等待脉冲高电平结束
                pass
            te=ticks_us()                   #结束时间
            tc=te-ts                        #回响时间（单位us，1us=1*10^(-6)s）
            distance=(tc*170)/10000         #距离计算 （单位为:cm）
        return distance