# ESP32_MicroPython_Note

基于MicroPython的ESP32单片机学习笔记


## 文件结构

```
|—— basic     # 点灯等基础操作
|  |—— 01_blink_led.py
|  |—— 02_timer.py
|  |—— 03_key.py
|  |—— 04_stop.py
|  |—— 05_voltage_measure.py
|  |—— 06_rtc_clock.py
|  |—— 07_pwm.py
|  |—— 08_uart.py

|—— sensors   # 各种传感器数据读取
|  |—— 01_DHT22   # DHT22温湿度传感器
|  |—— 02_BMP280  # 大气压传感器
|  |—— 03_HCSR04  # 超声波测距
|  |—— 04_HCSR505 # 人体感应
|  |—— 05_BH1750  # 光照度
|  |—— 06_ATK-NEO-6M    # GPS模块
|  |—— 土壤湿度传感器
|  |—— 水位传感器

|—— display   # 屏幕显示
|  |—— lcd15.py    # LCD屏显示内容
|  |—— ssd1306.py  # OLED屏驱动
|  |—— mian.py     # OLED屏测试

|—— communication # 通讯相关
|  |—— 01_WiFi            # 连接WiFi
|  |—— 02_Socket          # TCP双向通讯
|  |—— 03_MQTT_Publish    # MQTT向主题发布消息
|  |—— 03_MQTT_Subscribe  # MQTT订阅主题消息

|—— control   # 电机舵机控制

|—— examples  # 一些完成项目的实例
|  |—— weather_show

|—— bin       # 固件
|—— docs      # 文档
|—— images    # 图片
```

## `sensors`
各种传感器数据获取

### 06_ATK-NEO-6M

ATK-NEO-6M-V12（V12是版本号，下面均以ATK-NEO-6M 表示该产品）是一款高性能GPS定位模块。该模块采用U-BLOX NEO-6M模组，模块自带高性能无源陶瓷天线（无需再购买昂贵的有源天线了），并自带可充电后备电池（以支持温启动或热启动，后备电池在主电源断电后，可以维持半小时左右的GPS接收数据保存）。

模块通过串口与外部系统连接，串口波特率支持4800、9600、38400（默认）、57600等不同速率，兼容5V/3.3V单片机系统，可以非常方便的与您的产品进行连接。

模块配套上位机`u-center`

## `control`

实现控制电机,舵机等模块

### 01_L298N电机

接线
ESP32 - L298N
IO13    ENA
IO12    INT
IO14    INT2

电机模块可以使用单独电源,`dcmotor.py`为电机驱动程序,`main.py`为主程序


## `examples`

一些比较完整的项目

### Weather_Show

调用天气接口并通过lcd屏幕显示

### Temperature_Humidity

通过温湿度传感器获取环境温度和湿度信息
MQTT发布消息
在OLED屏显示温湿度数据及消息发布状态