import os
import RPi.GPIO as gp

gp.setwarnings(False)
gp.setmode(gp.BCM)

gp.setup(4, gp.OUT)
gp.setup(17, gp.OUT)
gp.setup(18, gp.OUT)

gp.setup(22, gp.OUT)
gp.setup(23, gp.OUT)
gp.setup(9, gp.OUT)
gp.setup(25, gp.OUT)

gp.output(17, True)
gp.output(18, True)
gp.output(22, True)
gp.output(23, True)
gp.output(9, True)
gp.output(25, True)

class Choosecam:
    def __init__(self,port):
        self.port = port

    def cam(self):
        if self.port == "A":
            i2c = "i2cset -y 1 0x70 0x00 0x04"  
            os.system(i2c)
            gp.output(4, False)
            gp.output(17, False)
            gp.output(18, True)
        elif self.port == "B":
            i2c = "i2cset -y 1 0x70 0x00 0x05"  
            os.system(i2c)
            gp.output(4, True)
            gp.output(17, False)
            gp.output(18, True)
        elif self.port == "C":
            i2c = "i2cset -y 1 0x70 0x00 0x06"  
            os.system(i2c)
            gp.output(4, False)
            gp.output(17, True)
            gp.output(18, False)
        elif self.port == "D":
            i2c = "i2cset -y 1 0x70 0x00 0x07"  
            os.system(i2c)
            gp.output(4, True)
            gp.output(17, True)
            gp.output(18, False)
            
    def end(self):
        gp.cleanup()


