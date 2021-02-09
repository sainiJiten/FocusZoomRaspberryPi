from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import os

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

temp_val = 30
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
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_CUBIC)
    cv2.imshow('Image', resized)
    rawCapture.truncate(0)
    key = cv2.waitKeyEx(1)
    if key == 65362:
        if temp_val < 1000:
            temp_val += 50
        value = (temp_val<<4) & 0x3ff0
        dat1 = (value>>8)&0x3f
        dat2 = value & 0xf0
        os.system("i2cset -y 1 0x0c %d %d" % (dat1,dat2))
        print("Zoom out f:",temp_val)
        
    elif key == 65364:
        if temp_val > 50:
            temp_val -= 50
        value = (temp_val<<4) & 0x3ff0
        dat1 = (value>>8)&0x3f
        dat2 = value & 0xf0
        os.system("i2cset -y 1 0x0c %d %d" % (dat1,dat2))
        print("Zoom in",temp_val)

    elif key == 65361 and scale>1:
        scale -= 1
        print("Scaled to",scale)

    elif key == 65363 and scale<5:
        scale += 1
        print("Scaled to",scale)

    elif key & 0xFF == ord('q'):
        break
        
cv2.destroyAllWindows()
