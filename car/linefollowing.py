import cv2
import numpy as np


import os


def midsearch(img):
    # cv2.imshow(filename,img)
    h,w,c= img.shape
    # print(h,w)
    mid=img[int(h*0.6):int(h),int(0.25*w):int(0.75*w)].copy()                            
    # cv2.imshow("mid",mid)
    # print(mid.shape)

    hm, wm, cm = mid.shape  
    gray = cv2.cvtColor(mid, cv2.COLOR_BGR2GRAY)                                      # cv2.imshow("gray",gray)
    ret, thre = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)  
    thre = cv2.medianBlur(thre, 11)

    # cv2.imshow("thre",thre)

    contours, hierarchy = cv2.findContours(thre, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # print(x, y, w, h)
        if h > 100:
            break

    x_sum = 0
    point_count = 0
    for point in contour:
        x_sum += point[0][0]
        point_count += 1
    x_mean = x_sum / point_count
    # print(x_mean)
    delta = ((x_mean - wm/2)/float(wm))*2
    print(x_mean, wm, type(delta), delta)

    cv2.drawContours(mid, [contour], -1, (0, 255, 0), 3)
    # cv2.imshow('contours', mid)


    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return delta


# for filename in os.listdir('images/test'):
#     img = cv2.imread("images/test/"+filename, -1) 
#     midsearch(img)


def midjudge(delta,pid):
    # L_v, R_v=9, 12  #
    # delta_L, delta_R = 3, 4
    # # right and need to turn right
    # if delta>=delta_thres:
    #     print("turn right")
    #     return   L_v+delta_L, R_v - delta_R
    # if delta_thres<= -delta_thres:
    #     print("turn left")
    #     return  L_v - delta_L,R_v + delta_R
    # if delta>-delta_thres and delta<delta_thres:
    #     if T<0:
    #         if T>= -90+T_thres:
    #             # Turn right
    #             print("turn right")
    #             return L_v + delta_L,R_v - delta_R
    #         else:
    #             return L_v,R_v
    #     if T>=0:
    #         if T<= 90 - T_thres:
    #             # Turn left
    #             print("turn left")
    #             return L_v - delta_L,R_v + delta_R
    #         else:
    #             return L_v,R_v
    # return L_v, R_v

    R_v=16
    L_v=12
    delta_v = pid.get_output(delta)

    if delta_v:
        return L_v+int(delta_v),R_v-int(delta_v*4/3)
    return L_v, R_v
