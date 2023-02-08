import machine

DEVICE_UUID = machine.unique_id()
DEVICE_UUID_STR = ''.join(['{:02x}'.format(b) for b in DEVICE_UUID])
DEVICE_NAME = 'esp32_' + DEVICE_UUID_STR
print('DEVICE_NAME: %s'%DEVICE_NAME)