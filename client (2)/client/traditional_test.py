import numpy as np
from img_udp_client import receive
from speed_udp_client import send_speed
from traditional import judge
import cv2
HOST = '192.168.223.77'
PORT = 7890

send_HOST = '192.168.223.167'
send_PORT = 6789
name=['other','crossing']
while True:
    img=receive(send_HOST,send_PORT)
    img=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    size=img.shape
    img=img[int(size[0]/4):size[0],:]
    if img is not None:
        print(name[judge(img)])