import numpy as np
from img_udp_client import receive
from speed_udp_client import send_speed
from circle import circle_extract
import torch
from torch import optim
from model import net
import cv2
HOST = '192.168.223.77'
PORT = 7890

send_HOST = '192.168.223.167'
send_PORT = 6789
id_to_label=["left","right"]
def test(img):
    img=torch.tensor(img,dtype=torch.float32)
    img=img.permute(2,1,0)
    img=img.reshape(1,img.shape[0],img.shape[1],img.shape[2])

    y=model(img)
    ans=torch.argmax(y)
    print(ans)
    print(id_to_label[ans])

model=net()
model.load_state_dict(torch.load('modelpth.pth'))
model.eval()
while True:
    img=receive(send_HOST,send_PORT)
    size=img.shape
    img=img[0:200,210:430]
    if img is not None:
        img=circle_extract(img,0)
        if img is not None:
            size=img.shape
            newimg=np.zeros((size[0],size[1],3))
            newimg[:,:,0]=img
            newimg[:,:,1]=img
            newimg[:,:,2]=img
            cv2.imshow('1',newimg)
            cv2.waitKey(1)
            test(newimg)