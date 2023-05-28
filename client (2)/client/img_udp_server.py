import socket
import time
import numpy as np
import cv2 

HOST = '192.168.27.83'
PORT = 5000


def bytes2cv(im):
    return cv2.imdecode(np.array(bytearray(im), dtype='uint8'), cv2.IMREAD_UNCHANGED)  # 从二进制图片数据中读取


def cv2bytes(im):
    return np.array(cv2.imencode('.png', im)[1]).tobytes()


def send(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024)
        

        while True:
            _, frame1 = cap1.read()
            image_data = cv2bytes(frame1)
            time_save = time.time()
            for i in range(0, len(image_data), 1024):
                s.sendto(image_data[i:i+1024], (HOST, PORT))
            print(f'Image sent successfully! {i//1024} bytes sent, cost {time.time() - time_save}s')
            time.sleep(0.1)
        s.close()


if __name__ == '__main__':
    cap1 = cv2.VideoCapture(0)
    send(HOST, PORT)
    # print(bytes2cv(cv2bytes(cv2.imread('test.png'))).shape)