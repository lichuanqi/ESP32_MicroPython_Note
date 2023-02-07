import machine
from machine import Pin,Timer
from time import sleep_ms

from micropython import const


# str to bytes
# 'str' -> b'str'
data = 'str'
data_bytes = bytes(data, 'utf-8')
print('str: %s -> bytes: %s'%(data, data_bytes))
print()


# bytes to str
# b'str' -> 'str'
data = b'str'
data_str = str(data, 'utf-8')
print('bytes: %s -> str: %s'%(data, data_str))
print()


# int to hex
# 17 -> 0x11
data_int = 17
data_hex = hex(data_int)
print('int: %s -> hex: %s'%(data_int, data_hex))
print()


# hex to int
# 0x11 -> 17
data_hex = 0x11
data_int = int(data_hex)
print('hex: %s -> int: %s'%(data_hex, data_int))
print()


# many bytes to many str
# b'\x08\xb6\x1f3T\xa4' -> 08 b6 1f 33 54 a4
data = b'\x08\xb6\x1f3T\xa4'
data_str = ' '.join(['{:02x}'.format(b) for b in data])
print('data many bytes: %s'%data)
print('data many strs: %s'%data_str)
print()


# many bytes to many int
# b'\x08\xb6\x1f3T\xa4' -> 8182315184164
data_hex = data_str.split(' ')
data_int = [int('0x'+bb) for bb in data_hex]
data_ints = ''.join([str(cc) for cc in data_int])
print('data many ints: %s'%data_ints)
print()