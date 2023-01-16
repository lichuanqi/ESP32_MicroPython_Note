from machine import I2C,Pin,SPI        #从machine模块导入I2C、Pin子模块
import framebuf
import micropython,gc

from ssd1306 import SSD1306_I2C
from ses266 import EPD


def display_by_ssd1306():
    i2c = I2C(sda=Pin(13), scl=Pin(14))   #I2C初始化：sda--> 13, scl --> 14
    oled = SSD1306_I2C(128, 64, i2c, addr=0x3c) #OLED显示屏初始化：128*64分辨率,OLED的I2C地址是0x3c

    oled.text("Hello World!", 0,  0)      #写入第1行内容
    oled.text("MicroPython",  0, 20)      #写入第2行内容
    oled.text("By 01Studio",  0, 50)      #写入第3行内容

    oled.show()   #OLED执行显示


def display_by_ses266():
    """SES 2.66 墨水屏测试"""
    # Display resolution
    EPD_WIDTH  = const(152)
    EPD_HEIGHT = const(296)
    black      = const(0)
    white      = const(1)
    # Display orientation
    ROTATE_0   = const(0)
    ROTATE_90  = const(1)
    ROTATE_180 = const(2)
    ROTATE_270 = const(3)
    
    
    e=EPD(spi=SPI(1,baudrate=10000000),cs=Pin(15),dc=Pin(4),rst=Pin(2),busy=Pin(5))
    e.init()
    
    
    buf_black=bytearray(EPD_WIDTH *EPD_HEIGHT//8)
    frb_black=framebuf.FrameBuffer(buf_black,EPD_WIDTH,EPD_HEIGHT,framebuf.MONO_HLSB)
    
    frb_black.fill(white)
    frb_black.text('Hello World',30,30,black)
    
    e.display_frame(buf_black)

if __name__ == '__main__':
    display_by_ssd1306()