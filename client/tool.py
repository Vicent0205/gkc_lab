import socket
import time
import numpy as np
import cv2 


def bytes2cv(im):
    return cv2.imdecode(np.array(bytearray(im), dtype='uint8'), cv2.IMREAD_UNCHANGED)  # 从二进制图片数据中读取


def cv2bytes(im):
    return np.array(cv2.imencode('.png', im)[1]).tobytes()