from machine import I2C,Pin
from mpu6050 import accel

i2c = I2C(scl=Pin("X9"), sda=Pin("X10"))
accel = accel(i2c)
accel_dict = accel.get_values()
print(accel_dict)