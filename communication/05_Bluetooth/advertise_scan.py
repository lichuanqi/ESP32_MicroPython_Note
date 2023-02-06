from machine import Pin,Timer
from time import sleep_ms
import bluetooth

from micropython import const

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)
_IRQ_GATTS_READ_REQUEST = const(4)
_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)
_IRQ_PERIPHERAL_CONNECT = const(7)
_IRQ_PERIPHERAL_DISCONNECT = const(8)
_IRQ_GATTC_SERVICE_RESULT = const(9)
_IRQ_GATTC_SERVICE_DONE = const(10)
_IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
_IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
_IRQ_GATTC_DESCRIPTOR_RESULT = const(13)
_IRQ_GATTC_DESCRIPTOR_DONE = const(14)
_IRQ_GATTC_READ_RESULT = const(15)
_IRQ_GATTC_READ_DONE = const(16)
_IRQ_GATTC_WRITE_DONE = const(17)
_IRQ_GATTC_NOTIFY = const(18)
_IRQ_GATTC_INDICATE = const(19)
_IRQ_GATTS_INDICATE_DONE = const(20)
_IRQ_MTU_EXCHANGED = const(21)
_IRQ_L2CAP_ACCEPT = const(22)
_IRQ_L2CAP_CONNECT = const(23)
_IRQ_L2CAP_DISCONNECT = const(24)
_IRQ_L2CAP_RECV = const(25)
_IRQ_L2CAP_SEND_READY = const(26)
_IRQ_CONNECTION_UPDATE = const(27)
_IRQ_ENCRYPTION_UPDATE = const(28)
_IRQ_GET_SECRET = const(29)
_IRQ_SET_SECRET = const(30)

_FLAG_BROADCAST = const(0x0001)
_FLAG_READ = const(0x0002)
_FLAG_WRITE_NO_RESPONSE = const(0x0004)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)
_FLAG_INDICATE = const(0x0020)
_FLAG_AUTHENTICATED_SIGNED_WRITE = const(0x0040)

_FLAG_AUX_WRITE = const(0x0100)
_FLAG_READ_ENCRYPTED = const(0x0200)
_FLAG_READ_AUTHENTICATED = const(0x0400)
_FLAG_READ_AUTHORIZED = const(0x0800)
_FLAG_WRITE_ENCRYPTED = const(0x1000)
_FLAG_WRITE_AUTHENTICATED = const(0x2000)
_FLAG_WRITE_AUTHORIZED = const(0x4000)


class ESP32_BLE():
    def __init__(self, name):
        self.name = name

        self.ble = bluetooth.BLE()
        self.ble.active(True)
        self.ble.config(gap_name=name)
        self.ble.irq(self.__irq)

        self.local_addr()
        self.register()

    def local_addr(self):
        addr_type, addr = self.ble.config('mac')
        print("local address: %s"%str(addr))

    def register(self):
        # Heart Rate
        HR_UUID = bluetooth.UUID(0x180D)
        HR_CHAR = (bluetooth.UUID(0x2A37), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,)
        HR_SERVICE = (HR_UUID, (HR_CHAR,),)
        
        # Nordic UART
        UART_UUID = bluetooth.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
        UART_TX = (bluetooth.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,)
        UART_RX = (bluetooth.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_WRITE,)
        UART_SERVICE = (UART_UUID, (UART_TX, UART_RX,),)

        SERVICES = (HR_SERVICE, UART_SERVICE,)
        ( (hr,), (tx, rx,), ) = self.ble.gatts_register_services(SERVICES)

    def advertiser(self):
        local_name = bytes(self.name, 'utf-8')
        manufacturer_data = bytes('humi=20,temp=12', 'utf-8')
        adv_data = b'\x02\x01\x02' +\
           bytearray((len(local_name)+1, 0x09)) + bytes(local_name, 'utf-8') +\
           bytearray((len(manufacturer_data)+1, 0xff)) + bytes(manufacturer_data, 'utf-8')
        resp_data = ''
        interval_us = 100
        
        print('strat advertiser: %s'%adv_data)
        if interval_us > 0:
            self.ble.gap_advertise(100, adv_data)


    def scan(self):
        duration_ms = 5000

        print('start scan')
        self.ble.gap_scan(duration_ms)

    def __irq(self, event, data):
        if event == _IRQ_SCAN_RESULT:
            # A single scan result.
            print(data)
            try:
                addr_type, addr, adv_type, rssi, adv_data = data
                print('A single scan result')
                print(addr_type, addr, adv_type, rssi, adv_data)
                print()
            except:
                pass

        elif event == _IRQ_SCAN_DONE:
            # Scan duration finished or manually stopped.
            print('scan completed')
            pass
        
        else:
            print("event: {}, data: {}".format(event, data))

if __name__ == "__main__":
    ble = ESP32_BLE("ESP32BLE")

    # 广播
    # ble.advertiser()

    # 扫描
    ble.scan()