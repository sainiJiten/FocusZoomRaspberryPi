from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import os
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from multicam import Choosecam

camera_select = Choosecam("B")
camera_select.cam()

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
channel0 = AnalogIn(mcp, MCP.P0)
channel1 = AnalogIn(mcp, MCP.P1)

pfd = 30
scale = 1


cv2.namedWindow("Image",cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Image",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

for fr in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = fr.array
    width = frame.shape[1]
    height = frame.shape[0]
    w = int(width/(2*scale))
    h = int(height/(2*scale))
    wc = int(width/2)
    hc = int(height/2)
    img = frame[hc-h:hc+h,wc-w:wc+w,:]
    wi = int(img.shape[1]*scale)
    hi = int(img.shape[0]*scale)
    dim = (wi,hi)
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_LINEAR)
    cv2.imshow('Image', resized)
    rawCapture.truncate(0)
    scale = int(np.round(channel0.voltage*1.2)) + 1
    print("Scale:",scale)
    cfd = int(np.round(channel1.voltage*293.9)) + 30
    if pfd != cfd:
        value = (cfd<<4) & 0x3ff0
        dat1 = (value>>8)&0x3f
        dat2 = value & 0xf0
        os.system("i2cset -y 0 0x0c %d %d" % (dat1,dat2))
        print("Focal Length:",cfd)
        pfd = cfd

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cv2.destroyAllWindows()
