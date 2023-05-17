# client pc

import socket
import numpy as np
import cv2

from linefollowing import *
from tool import *
from test import entry
from speed_udp_client import send_speed

recv_HOST = '192.168.223.83' # pc
recv_PORT = 6789

send_HOST = '192.168.223.77' # shump ip
send_PORT = 7890

def receive(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as c:
        c.bind((HOST, PORT))

        c.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1000000)
        cnt_receive = 0
        pid = PID_Controller(9, 0.05, 0)
        while True:
            cnt_print = 0
            
            image_data = b''
            while True:
                data, addr = c.recvfrom(1024)
                image_data += data
                # if cnt_print % 100 == 0:
                #     print(cnt_print, len(data))
                cnt_print += 1
                if len(data) < 1024:
                    break

            # 将图片数据写入文件

            img = bytes2cv(image_data)
            # print(type(img))
            if img is not None:
                entry(img)
                if midsearch(img):
                    delta,T = midsearch(img)
                    Lv, Rv = midjudge(delta, T, pid)
                    send_speed(send_HOST, send_PORT, Rv=Rv, Lv=Lv)#第一个右轮，第二个左轮
                # 打印接收成功信息
                    # print(f'Image {cnt_receive} received successfully! receive {cnt_print*1024} bytes, Lv: {Lv}, Rv: {Rv}')

                    with open(f'images/received_image{cnt_receive}_%.2f_{Lv}_{Rv}.png'%delta, 'wb') as f:
                        f.write(image_data)

            cnt_receive += 1

if __name__ == '__main__':
    receive(recv_HOST, recv_PORT)