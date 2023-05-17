import torch
from torch import optim
from model import net
from dataset import LiverDataset
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
from torch import nn
import numpy as np
from client import receive
from speed_udp_client import send_speed
HOST = '192.168.27.83'
PORT = 5000

send_HOST = '192.168.27.77'
send_PORT = 7890
def test():
    model=net()
    model.load_state_dict(torch.load('model.pth'))
    model.eval()
    img=receive(HOST,PORT)

    y=model(img)
    y=torch.argmax(y)
    y=str(y)
    send_data=y.encode()
    send_speed(send_HOST,send_PORT,send_data)

