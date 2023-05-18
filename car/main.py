from linefollowing import *
import time
import cv2
import numpy as np
# from driver import driver
from threading import Thread
import threading
import socket

send_HOST = '10.181.250.31' # pc ip, send img
send_PORT = 6789 
recv_HOST = '10.181.250.31' # shumeipai ip, recv speed
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


def cv2bytes(im):
    return np.array(cv2.imencode('.png', im)[1]).tobytes()


def send(image_data, HOST, PORT,time_save):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024)
    
    for i in range(0, len(image_data), 1024):
        s.sendto(image_data[i:i+1024], (HOST, PORT))
        # time.sleep(0.02)
    print('Image sent successfully! cost {}s'.format(time.time() - time_save))
    s.close()

def send_img(cap1,send_HOST,send_PORT):
    global stop_event
   
    while not stop_event.is_set():
    
        time_save = time.time()
        ret, frame1 = cap1.read()
        if ret:
        # print(type(frame1))
            image_data = cv2bytes(frame1)
            # print('img sending...')
            send(image_data, send_HOST, send_PORT,time_save)
            # time.sleep(0.5)


def main(cap1):
    # car = driver()
    global stop_event
    pid = PID_Controller(7.5, 0.05, 0)
    
    while not stop_event.is_set():
        # text=open("crossing.txt",'r')
        text=open("crossing.txt",'r')
        crossing= text.read()
        
        print(crossing)
        if (crossing == '0' or crossing==''):
            # print("drive normally")
            ret, img = cap1.read()
            if ret:
                delta =midsearch(img)
                Lv,Rv =midjudge(delta,pid)
                print("Right {}, left {}".format(Rv,Lv))
                # car.set_speed(Rv ,Lv)
                
            
        else:
            print("detect a crossing!")
            #####################  insert the part of turning left or turning right ############

            ###################################################################################
        text.close()
    # except KeyboardInterrupt:
    #     # is_running=False
    #     cap1.release()
    #     pass


stop_event = threading.Event()


if __name__=="__main__":
    cap1 = cv2.VideoCapture(0)
    
    stop_event = threading.Event() 
    t1 = Thread(target=send_img,args=(cap1,send_HOST,send_PORT))
    
    t2 = Thread(target=main, args=(cap1,))
    
    t1.start()
    
    t2.start()

    
    input("press Enter to stop the program \n")

    stop_event.set()
    is_running = False

   
    t1.join()
    t2.join()

    cap1.release()

    # main(cap1)
    # cap1.release()
    
    
