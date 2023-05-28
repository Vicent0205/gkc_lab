import torch
from torch import optim
from model import net
#from dataset import LiverDataset
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
from torch import nn
import numpy as np
from img_udp_client import receive
from speed_udp_client import send_speed
HOST = '192.168.223.77'
PORT = 7890

send_HOST = '192.168.223.167'
send_PORT = 6789

id_to_label=["crossing","other"]
def test(img):
    img=torch.tensor(img,dtype=torch.float32)
    img=img.permute(2,1,0)
    img=img.reshape(1,img.shape[0],img.shape[1],img.shape[2])

    y=model(img)
    ans=torch.argmax(y)
    print(ans)
    print(id_to_label[ans])

model=net()
model.load_state_dict(torch.load('model.pth'))
model.eval()
while True:
    img=receive(send_HOST,send_PORT)
    if img is not None:
        size=img.shape
        img=img[int(size[0]/4):size[0],:]
        '''
        y=model(img)
        y=torch.argmax(y)
        y=str(y)
        send_data=y.encode()
        send_speed(send_HOST,send_PORT,send_data)'''
        test(img)