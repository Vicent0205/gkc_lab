import numpy as np
import socket
import cv2
from driver import driver
from threading import Thread
from cameraTest import *

car = driver()
V0, V1=0, 0
def server():
        
    while True :
        global V0,V1
        text= open('crossing.txt','w+')
        
        crossing = receive(recv_HOST, recv_PORT)
        text.write(crossing)
        print('crossing: {}'.format(crossing))
        # car.set_speed(speed[0], speed[1])
        text.close()
        
    
    return crossing

def set_speed(speed0,speed1):
    global V0,V1
    while True:
        car.set_speed(V0, V1)


def one_same():
    #x = 40
    #y = 30
    x=20
    y=15
    return x, y


def diff_left():
    x = 40
    y = 80
    return x, y


def diff_right():
    x = 80
    y = 40
    return x, y

if __name__ == '__main__':
    '''
    t1 = Thread(target=server)
    t2 = Thread(target=set_speed, args=(V0, V1))


    t1.start()
    t2.start()


    t1.join()
    t2.join()'''
    
    server()
    #for i in range(20): car.set_speed(diff_left()[0], diff_left()[1])

    #for i in range(20): car.set_speed(diff_right()[0], diff_right()[1])

