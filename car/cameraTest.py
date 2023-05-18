import socket
import numpy as np
import time
import cv2 
from main import stop_event

send_HOST = '10.181.250.31' # pc ip, send img
send_PORT = 6789 
recv_HOST = '10.181.250.31' # shumeipai ip, recv speed
recv_PORT = 7890


def bytes2cv(im):
    return cv2.imdecode(np.array(bytearray(im), dtype='uint8'), cv2.IMREAD_UNCHANGED)  


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

def receive(HOST, PORT):
    server = socket.socket(type=socket.SOCK_DGRAM)
    server.bind((HOST, PORT))
    recv_data, address = server.recvfrom(1024)
    if not recv_data:
        print('no data!')
    data = recv_data.decode("utf-8")
    print(data, type(data))
    server.close()
    
    return data

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
    



if __name__ == '__main__':
    cap1 = cv2.VideoCapture(0)
    send_img(cap1,send_HOST,send_PORT)
        







