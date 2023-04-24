import socket
import numpy as np
import cv2
import time

HOST = '192.168.27.83'
PORT = 5000
def bytes2cv(im):
    return cv2.imdecode(np.array(bytearray(im), dtype='uint8'), cv2.IMREAD_UNCHANGED)  # 从二进制图片数据中读取

def receive(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as c:
        c.bind((HOST, PORT))

        c.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1000000)
        cnt_receive = 0
        while True:
            cnt_print = 0
            
            image_data = b''
            while True:
                data, addr = c.recvfrom(1024)
                image_data += data
                if cnt_print % 100 == 0:
                    print(cnt_print, len(data))
                cnt_print += 1
                if len(data) < 1024:
                    break

            # 将图片数据写入文件
            with open(f'images/received_image_{cnt_receive}.png', 'wb') as f:
                f.write(image_data)

            # 打印接收成功信息
            print(f'Image {cnt_receive} received successfully! receive {cnt_print*1024} bytes')
            time.sleep(0.05)
            cnt_receive += 1
            image=bytes2cv(image_data)
            return image
        c.close()
if __name__ == '__main__':
    receive(HOST, PORT)