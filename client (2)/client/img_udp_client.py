# client pc
import sys
import socket
import numpy as np
import cv2
import time
from tkinter import *
from tkinter.filedialog import askopenfilename
from linefollowing1 import *
from tool import *
from speed_udp_client import send_speed,send_crossing
from threading import Thread
from PIL import Image, ImageTk
import torch
from torch import optim
from model import net
recv_HOST = '192.168.43.14' # pc
recv_PORT = 6789

send_HOST = '192.168.43.147' # shump ip
send_PORT = 7890

REC_IMG=None  # 全局变量：接收到的图片
SUB_IMG=None  # 全局变量：处理中间过程图片
V=[0,0]       # 小车速度：全局变量
ON=True       # 服务器运行开关

def test(img):
    img=torch.tensor(img,dtype=torch.float32)
    img=img.permute(2,1,0)
    img=img.reshape(1,img.shape[0],img.shape[1],img.shape[2])

    y=model(img)
    ans=torch.argmax(y)
    return ans

def receive(HOST, PORT):
    global REC_IMG,SUB_IMG,V,ON
    count=0
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as c:
        c.bind((HOST, PORT))
        print("bind done")
        c.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1000000)
        cnt_receive = 0

        pid = PID_Controller(9, 0.05, 0)

        while ON:
            cnt_print = 0
            
            image_data = b''
            while ON:
                data, addr = c.recvfrom(1024)
                image_data += data
                # if cnt_print % 100 == 0:
                #     print(cnt_print, len(data))
                cnt_print += 1
                if len(data) < 1024:
                    break

            # 将图片数据写入文件
            # with open(f'client/images/others/received_image_{cnt_receive}.png', 'wb') as f:
            #     f.write(image_data)
            img = bytes2cv(image_data)
            print(type(img))
            if img is not None:
                REC_IMG=img
                #cv2.imshow('1',img)
                #cv2.waitKey(1)
                print(img.shape)
                #################### 判断路口和标志 ##################
                #crossing= (cnt_receive//5)%2
                
                size=img.shape
                newimg=np.zeros((size[0],size[1],3))
                newimg[:,:,0]=img
                newimg[:,:,1]=img
                newimg[:,:,2]=img
                cv2.imwrite("obj/"+str(count)+".jpg",newimg)
                count+=1
                crossing=(test(newimg)+1).item()
                print("crossing "+str(crossing))
                #####################################################
                

                # if midsearch(img):
                #     delta,SUB_IMG = midsearch(img)
                    
                #     Lv, Rv = midjudge(delta, pid)
                #     V[0],V[1]=Rv,Lv

                send_crossing(send_HOST, send_PORT, crossing)  # 发送路口信息
                # 打印接收成功信息
                print(f'Image {cnt_receive} received successfully! receive {cnt_print*1024} bytes')
            time.sleep(0.05)
            cnt_receive += 1


class CarWindow:
    def __init__(self, win, ww, wh):
        global REC_IMG,SUB_IMG,V
        self.win = win
        self.ww = ww
        self.wh = wh
        self.win.geometry("%dx%d+%d+%d" % (ww, wh, 200, 50))  # 界面启动时的初始位置
        self.win.title("车牌定位，矫正和识别软件")
        self.img_src_path = None

        self.label_src = Label(self.win, text='原图:', font=('微软雅黑', 13)).place(x=0, y=0)
        self.label_lic1 = Label(self.win, text='巡线画布:', font=('微软雅黑', 13)).place(x=100, y=520)
        self.label_pred1 = Label(self.win, text='车轮速度:', font=('微软雅黑', 13)).place(x=350, y=520)
        
        self.src=REC_IMG
        self.can_src = Canvas(self.win, width=500, height=650, bg='white', relief='solid', borderwidth=1)  # 视频画面
        self.can_src.place(x=50, y=0)

        self.subfig=SUB_IMG
        self.can_lic1 = Canvas(self.win, width=405, height=300, bg='white', relief='solid', borderwidth=1)  # 巡线画布
        self.can_lic1.place(x=50, y=545)
        self.v=V
        self.can_pred1 = Canvas(self.win, width=245, height=65, bg='white', relief='solid', borderwidth=1)  # 车轮速度画布
        self.can_pred1.place(x=315, y=545)

        self.button1 = Button(self.win, text='开始/停止', width=10, height=1, command=self.changeON)  # 选择文件按钮
        self.button1.place(x=ww-300, y=650)

        self.button2 = Button(self.win, text='同步信息', width=10, height=1, command=self.load_data)  # 识别车牌按钮
        self.button2.place(x=ww-200, y=650)

        self.win.after(200,self.load_data)
        self.HOST = '192.168.43.14' # pc
        self.PORT = 6789

    def load_data(self):
        
        global REC_IMG,SUB_IMG,V,ON
        self.clear()
        self.can_pred1.create_text(47, 15, text='右轮：{} 左轮：{}'.format(self.v[0],self.v[1]), anchor='nw', font=('黑体', 15))
        # print(str(type(REC_IMG) )=="<class 'numpy.ndarray'>")
        if str(type(REC_IMG)) =="<class 'numpy.ndarray'>":
            # print(type(REC_IMG))
            
            img = Image.fromarray(REC_IMG[:, :, ::-1])  
            self.src=ImageTk.PhotoImage(img)
            
            self.can_src.create_image(240, 320, image=self.src, anchor='center')

        if str(type(SUB_IMG)) =="<class 'numpy.ndarray'>":    
            img = Image.fromarray(SUB_IMG[:, :, ::-1])
            self.subfig=ImageTk.PhotoImage(img)
            self.can_lic1.create_image(5, 5, image=self.subfig,anchor='nw')

        self.win.after(200,self.load_data)
        
    def changeON(self):
        global ON
        if ON==True:
            ON=False
        else:
            ON=True
    
    def clear(self):
        self.can_src.delete('all')
        self.can_lic1.delete('all')
        
        self.can_pred1.delete('all')


    def closeEvent():  # 关闭
        
        sys.exit()


def runwindow():
    win = Tk()
    ww = 800  # 窗口宽设定600
    wh = 900  # 窗口高设定700
    CarWindow(win, ww, wh)
    win.protocol("WM_DELETE_WINDOW", CarWindow.closeEvent)
    win.mainloop()



if __name__ == '__main__':
    model=net()
    model.load_state_dict(torch.load('modelpth.pth'))
    model.eval()
    # receive(recv_HOST, recv_PORT)
    #t1 = Thread(target=runwindow)
    
    receive(recv_HOST, recv_PORT)


    # #t1.start()
    # t2.start()


    # #t1.join()
    # t2.join()
    