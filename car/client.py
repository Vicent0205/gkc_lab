import numpy as np
import socket
import cv2
# from driver import driver
from threading import Thread
from cameraTest import *

# car = driver()
V0, V1=0, 0
def server():
        
    while True :
        global V0,V1
        text= open('crossing.txt','w')
        
        crossing = receive(recv_HOST, recv_PORT)
        text.write(str(crossing))
        print('crossing: {}'.format(crossing))
        # car.set_speed(speed[0], speed[1])
        text.close()
        time.sleep(0.5)
        
    
    return crossing



if __name__ == '__main__':
  
    server()
   

