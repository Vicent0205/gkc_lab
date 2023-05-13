#server
import socket
import cv2
import numpy as np
server = socket.socket(type=socket.SOCK_DGRAM)
server.bind(("10.180.104.19", 7890))

recv_data, address = server.recvfrom(1024)
data = recv_data.decode("utf-8")
speed = [int(i) for i in data.split(' ', 1)]
print(speed, type(speed[0]))
# img = cv2.imread('img/5.png')
# img_encode = cv2.imencode('.png',img,[cv2.IMWRITE_JPEG_QUALITY, 99])
# server.sendto(img_encode.tobytes(), address)
# print(address)
server.close()
