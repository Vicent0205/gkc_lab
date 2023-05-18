from linefollowing import *
import time
import cv2
import numpy as np
from driver import driver
from threading import Thread
from cameraTest import *

send_HOST = '192.168.43.14' # pc ip, send img
send_PORT = 6789 
recv_HOST = '192.168.43.147' # shumeipai ip, recv speed
recv_PORT = 7890


class PID_Controller:
    def __init__(self,kp,ki,kd,output_min=-20,output_max=20):
        
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.error = 0 
        self.last_error = 0 
        self.error_sum = 0 
        self.error_diff = 0 
        
        
        self.output_min = output_min
        self.output_max = output_max
        self.output = 0 

    def constrain(self, output):
        
        
        if self.error_sum > 8:
            self.error_sum = 0
        if output > self.output_max:
            output = self.output_max
        elif output < self.output_min:
            output = self.output_min
        else:
            output = output
        return output

    def get_output(self, error):
        
        self.error = error
        self.error_sum += self.error 
        self.error_diff = self.error - self.last_error 
        self.last_error = self.error

        output = self.kp * self.error + self.ki * self.error_sum + self.kd * self.error_diff
        self.output = self.constrain(output)

        return self.output


def main(cap1):
    car = driver()
    pid = PID_Controller(7.5, 0.05, 0)
    try:
        while True:
            text=open("crossing.txt",'r')
            crossing= text.read()
            text.close()
            if (crossing == '0' or crossing==''):
                print("drive normally")
                ret, img = cap1.read()
                if ret:
                    delta =midsearch(img)
                    Lv,Rv =midjudge(delta,pid)
                    print("Right {}, left {}".format(Rv,Lv))
                    car.set_speed(Rv ,Lv)
                    
                
            else:
                print("detect a crossing!")
    except KeyboardInterrupt:
        cap1.release()
        pass


if __name__=="__main__":
    cap1 = cv2.VideoCapture(0)
    
    '''t1 = Thread(target=send_img,args=(cap1,send_HOST,send_PORT))
    
    t2 = Thread(target=main, args=(cap1,))
    
    t1.start()
    t2.setDaemon(True)
    t2.start()

    t1.join(5)
    t2.join(5)'''
    main(cap1)
    cap1.release()
    
    
