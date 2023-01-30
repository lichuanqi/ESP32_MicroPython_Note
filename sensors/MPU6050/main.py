"""

参数解析
六轴MPU6050输出所有参数：

加速度计的X轴分量：ACC_X
加速度计的Y轴分量：ACC_Y
加速度计的Z轴分量：ACC_Z
当前温度：TEMP
绕X轴旋转的角速度：GYR_X
绕Y轴旋转的角速度：GYR_Y
绕Z轴旋转的角速度：GYR_Z

MPU6050芯片的座标系是这样定义的：令芯片表面朝向自己，
将其表面文字转至正确角度，此时，以芯片内部中心为原点，
水平向右的为X轴，竖直向上的为Y轴，指向自己的为Z轴。
"""

from machine import I2C,Pin


i2c = I2C(scl=Pin("X9"), sda=Pin("X10"))
accel = mpu6050.accel(i2c)
accel_dict = accel.get_values()
print(accel_dict)