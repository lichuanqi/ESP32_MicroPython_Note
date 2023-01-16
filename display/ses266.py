from micropython import const
from time import sleep_ms
import ustruct
import math
 
# Display resolution
EPD_WIDTH  = const(152)
EPD_HEIGHT = const(296)
 
# Display commands
PANEL_SETTING                     = const(0x00)
POWER_OFF                         = const(0x02)
POWER_ON                          = const(0x04)
BOOSTER_SOFT_START                = const(0x06)
DEEP_SLEEP                        = const(0x07)
DATA_START_TRANSMISSION_1         = const(0x10)
DISPLAY_REFRESH                   = const(0x12)
DATA_START_TRANSMISSION_2         = const(0x13)
VCOM_AND_DATA_INTERVAL_SETTING    = const(0x50)
TCON_RESOLUTION                   = const(0x61)
VCM_DC_SETTING_REGISTER           = const(0x82)
UNKNOWN_CMD                       = const(0x92)
 
# Display orientation
ROTATE_0   = const(0)
ROTATE_90  = const(1)
ROTATE_180 = const(2)
ROTATE_270 = const(3)
 
 
#BUSY = const(0)  # 0=busy, 1=idle
BUSY = const(1)  # 0=idle, 1=busy
#rstPin-->low=active
#dc------>low=command
#cs------>low=active
 
 
 
 
 
class EPD:
    def __init__(self,spi,cs,dc,rst,busy):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.busy = busy
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=0)
        self.busy.init(self.busy.IN)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self.rotate = ROTATE_0
        
    def _command(self,command,data=None):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([command]))
        self.cs(1)
        if data is not None:
            self._data(data)
    
    def _data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(data)
        self.cs(1)
        
    def init(self):
        self.reset()
        self._command(BOOSTER_SOFT_START,b'\x17\x17\x17')# BOOSTER_SOFT_START
        
        self._command(POWER_ON)
        self.wait_until_idle()
        
        self._command(PANEL_SETTING, b'\xCF') # (296x160, LUT from register, B/W/R run both LU1 LU2, scan up, shift right, bootster on) KW-BF   KWR-AF    BWROTP 0f
        self._command(VCOM_AND_DATA_INTERVAL_SETTING, b'\x77')
        self._command(TCON_RESOLUTION,b'\x98\x01\x28')
        self._command(VCM_DC_SETTING_REGISTER, b'\x0A')
        
        #self._command(PLL_CONTROL, b'\x3A') # 3A 100HZ   29 150Hz 39 200HZ    31 171HZ
        #self._command(POWER_SETTING, b'\x03\x00\x2b\x2b\x09') # VDS_EN VDG_EN, VCOM_HV VGHL_LV[1] VGHL_LV[0], VDH, VDL, VDHR
        #self._command(BOOSTER_SOFT_START, b'\x07\x07\x17')
        #self._command(POWER_OPTIMIZATION, b'\x60\xA5')
        #self._command(POWER_OPTIMIZATION, b'\x89\xA5')
        #self._command(POWER_OPTIMIZATION, b'\x90\x00')
        #self._command(POWER_OPTIMIZATION, b'\x93\x2A')
        #self._command(POWER_OPTIMIZATION, b'\x73\x41')
        #self._command(VCM_DC_SETTING_REGISTER, b'\x12')
        #self._command(VCOM_AND_DATA_INTERVAL_SETTING, b'\x87') # define by OTP
        #self.set_lut()
        #self._command(PARTIAL_DISPLAY_REFRESH, b'\x00')
        #self.turnOnDisplay()
        
    def reset(self):
        self.rst(0)
        sleep_ms(200)
        self.rst(1)
        sleep_ms(200)        
        
    def wait_until_idle(self):
        while self.busy.value() == BUSY:
            print("waiting for busy...")
            sleep_ms(50)        
        
    def turnOnDisplay(self):
        self._command(DISPLAY_REFRESH)
        self.wait_until_idle()
 
 
    def display_frame(self, frame_buffer_black, frame_buffer_red):
        #self._command(TCON_RESOLUTION, ustruct.pack(">HH", EPD_WIDTH, EPD_HEIGHT))#写分辨率，已在init中，不用再写
        if (frame_buffer_black != None):
            self._command(DATA_START_TRANSMISSION_1)#写黑白
            sleep_ms(2)
            for i in range(0, self.width * self.height // 8):
                self._data(bytearray([frame_buffer_black[i]]))
                #print(i)
            sleep_ms(2)
            self._command(UNKNOWN_CMD);#???
        if (frame_buffer_red != None):
            self._command(DATA_START_TRANSMISSION_2)#写红色
            sleep_ms(2)
            for i in range(0, self.width * self.height // 8):
                self._data(bytearray([frame_buffer_red[i]]))
            sleep_ms(2)
            self._command(UNKNOWN_CMD);#???
        self.turnOnDisplay()