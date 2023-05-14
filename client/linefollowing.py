import cv2
import numpy as np
import matplotlib.pyplot as plt
import pylab
 
COLOR_THRESH = {'black': {'lower': (0,0,0), 'upper': (180, 255, 80)}}

def midsearch(img):
    # img = cv2.imread("curve85.jpg", -1)                                                   #导入图片，参数请自行修改
    h,w,c= img.shape
    # print(h,w)
    mid=img[int(h*0.7):int(h),int(0.25*w):int(0.75*w)]                            #ROI选区，选择图像前面的一块区域
    hm, wm, cm = mid.shape  

    # hsv = cv2.cvtColor(mid, cv2.COLOR_BGR2HSV)
    # mask = cv2.inRange(hsv, COLOR_THRESH['black']['lower'], COLOR_THRESH['black']['upper'])

    gray = cv2.cvtColor(mid, cv2.COLOR_BGR2GRAY)                                  #设置图像为灰度图
    ret, gray = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)  #大津法二值化
    gray = cv2.medianBlur(gray, 11)                                                #高斯滤波
    
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    orgb = cv2.cvtColor(mid, cv2.COLOR_BGR2RGB)
    oShow = orgb.copy()
    # cv2.imshow("666",edges)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 1, minLineLength=20, maxLineGap=30)#边缘检测之后霍夫变换得出直线
    fn=0
    n=0
    tan=0
    T=0.0   # 斜率
    delta=0 # 线相对于图像中心的偏移量
    # print(lines)
    if lines is not None:
        for line in lines:
            print(line)
            x1, y1, x2, y2 = line[0]
            cv2.line(orgb, (x1, y1), (x2, y2), (255, 0, 0), 2)
            n+=2
            fn+=x1
            fn+=x2
            if x1!=x2:
                tan+=(y1-y2)/(x1-x2)
            else:
                tan=99                                       #通过检测直线斜率检测是否遇到直角
        average=fn/n
        delta=(average-wm/2)/wm  

        T=np.arctan(tan/len(lines))/np.pi*180
        print(f'delta: {delta}, T: {T}')

    plt.subplot(121)
    plt.imshow(orgb)
    plt.axis('off')
    plt.subplot(122)
    plt.imshow(edges)
    plt.axis('off')
    pylab.show()
    return delta,T



def midjudge(delta,T,delta_thres=0.13,T_thres=8):
    R_v=12  #右轮：左轮4:3
    L_v=9

    if delta==0 and T==0: # 检测失败
        return L_v/3,R_v/3 #缓慢直行



    # right and need to turn right
    if delta>=delta_thres:
        print("turn right")
        return   L_v+1.5,R_v
    if delta_thres<= -delta_thres:
        print("turn left")
        return  L_v,R_v+2
    if delta>-delta_thres and delta<delta_thres:
        if T<0:
            if T>= -90+T_thres:
                # Turn right
                print("turn right")
                return L_v+1.5,R_v
            else:
                return L_v,R_v
        if T>=0:
            if T<= 90 - T_thres:
                # Turn left
                print("turn left")
                return L_v,R_v+2
            else:
                return L_v,R_v
    return L_v, R_v
        



if __name__=="__main__":
    img= cv2.imread('./testimg/curve139.jpg')
    midsearch(img)

 
# delta,T=midsearch()
# midjudge(delta,T)
# cv2.waitKey(0)
# cv2.destroyAllWindows()