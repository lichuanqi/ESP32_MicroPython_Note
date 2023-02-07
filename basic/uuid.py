import machine

device_uuid = machine.unique_id()
device_uuid_str = ''.join(['{:02x}'.format(b) for b in device_uuid])
print('device_uuid: %s'%device_uuid)
print('device_uuid_str: %s'%device_uuid_str)