# ESP32_MicroPython_Note

基于MicroPython的ESP32单片机学习笔记


## 文件结构

```
|- basic     # 点灯等基础操作
|- |- 01_blink_led.py
|- |- 02_timer.py
|- |- 03_key.py
|- |- 04_stop.py
|- |- 05_voltage_measure.py
|- |- 06_rtc_clock.py
|- |- 07_pwm.py
|- |- 08_uart.py

|- sensors   # 各种传感器数据读取
|- |- 01_DHT22  # DHT22温湿度传感器
|- |- 02_BMP280 # 大气压传感器
|- |- 03_HCSR04 # 超声波测距
|- |- 04_

|- display   # 屏幕显示
|- |- lcd15.py    # LCD屏显示内容
|- |- ssd1306.py  # OLED屏驱动
|- |- mian.py     # OLED屏测试

|- communication # 通讯相关
|- |- 01_WiFi            # 连接WiFi
|- |- 02_Socket          # TCP双向通讯
|- |- 03_MQTT_Publish    # MQTT向主题发布消息
|- |- 03_MQTT_Subscribe  # MQTT订阅主题消息

|- control   # 电机舵机控制

|- examples  # 一些完成项目的实例
|- |- weather_show

|- bin       # 固件
|- docs      # 文档
|- images    # 图片
```

## 项目

### `weather_show`


### `Temperature_Humidity`

温湿度传感器通过MQTT发布消息