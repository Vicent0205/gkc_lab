import os
import torch
from torch import nn
class_dim=2


class net(nn.Module):
    def __init__(self):
        super(net,self).__init__()
        self.net_in=nn.Sequential(
            nn.Conv2d(3,16,kernel_size=5,stride=1,padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2,stride=2),
            nn.Conv2d(16,32,kernel_size=5,stride=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2,stride=2),
            nn.Conv2d(32,64,kernel_size=5,stride=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2,stride=2),
            nn.Flatten(),
            nn.Linear(16384,1024),nn.ReLU(),
            #nn.Dropout(p=0.1),
            nn.Dropout(p=0.3),
            nn.Linear(1024,class_dim) 
        )
    def forward(self,x):
        return self.net_in(x)
if __name__ =='__main__':
    X=torch.randn(1,3,160,160)
    myNet=net()
    print(myNet(X))
