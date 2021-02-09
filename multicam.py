import os
import RPi.GPIO as gp

gp.setwarnings(False)
gp.setmode(gp.BOARD)

gp.setup(7, gp.OUT)
gp.setup(11, gp.OUT)
gp.setup(12, gp.OUT)

gp.setup(15, gp.OUT)
gp.setup(16, gp.OUT)
gp.setup(21, gp.OUT)
gp.setup(22, gp.OUT)

gp.output(11, True)
gp.output(12, True)
gp.output(15, True)
gp.output(16, True)
gp.output(21, True)
gp.output(22, True)

class Choosecam:
    def __init__(self,port):
        self.port = port

    def cam(self):
        if self.port == "A":
            i2c = "i2cset -y 1 0x70 0x00 0x04"  
            os.system(i2c)
            gp.output(7, False)
            gp.output(11, False)
            gp.output(12, True)
        elif self.port == "B":
            i2c = "i2cset -y 1 0x70 0x00 0x05"  
            os.system(i2c)
            gp.output(7, True)
            gp.output(11, False)
            gp.output(12, True)
        elif self.port == "C":
            i2c = "i2cset -y 1 0x70 0x00 0x06"  
            os.system(i2c)
            gp.output(7, False)
            gp.output(11, True)
            gp.output(12, False)
        elif self.port == "D":
            i2c = "i2cset -y 1 0x70 0x00 0x07"  
            os.system(i2c)
            gp.output(7, True)
            gp.output(11, True)
            gp.output(12, False)
            
    def end(self):
        gp.output(7, False)
        gp.output(11, False)
        gp.output(12, True)


