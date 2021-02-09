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
from multicam_bcm import Choosecam

def focusing(val):
    value = (val << 4) & 0x3ff0
    data1 = (value >> 8) & 0x3f
    data2 = value & 0xf0
    os.system("i2cset -y 1 0x0c %d %d" % (data1,data2))
    

def laplacian(img):
    img_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    return cv2.Laplacian(img_gray, cv2.CV_64F).var()

camera_select = Choosecam("C")
camera_select.cam()

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(640,480))
time.sleep(0.1)

spi = busio.SPI(clock=board.SCK_1, MISO=board.MISO_1, MOSI=board.MOSI_1)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
channel0 = AnalogIn(mcp, MCP.P0)

focal_distance = 30
scale = 1
flag = 0
count = 0

cv2.namedWindow("Image",cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Image",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

for fr in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = fr.array
    val = laplacian(frame)
    print("Laplacian Value:",val)
    if val < 35 and flag == 0 and focal_distance < 1000:
        focusing(focal_distance)
        print("focal distance:",focal_distance)
        focal_distance += 50
    elif val < 35 and flag == 1:
        count += 1
        if count == 6:
            flag = 0
            count = 0
    else:
        flag = 1
        focal_distance = 30
        count = 0

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
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_CUBIC)
    cv2.imshow('Image', resized)
    rawCapture.truncate(0)
    scale = int(np.round(channel0.voltage*1.2)) + 1
    print("Scale:",scale)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()
camera_select.end()
