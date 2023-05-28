import cv2
import numpy as np
import os
def img_match(img):
    path_left='template/left/'
    path_right='template/right/'
    name_left=os.listdir(path_left)
    name_right=os.listdir(path_right)
    left_score=0.0
    right_score=0.0
    for i in name_left:
        file_path=path_left+i
        template=cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), flags=cv2.IMREAD_COLOR)
        template=cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
        ret, template=cv2.threshold(template, 0, 255, cv2.THRESH_OTSU)
        template=255-template
        result=cv2.matchTemplate(img,template,cv2.TM_CCOEFF)
        left_score+=result[0][0]
    for i in name_right:
        file_path=path_right+i
        template=cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), flags=cv2.IMREAD_COLOR)
        template=cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
        ret, template=cv2.threshold(template, 0, 255, cv2.THRESH_OTSU)
        #template=255-template
        result=cv2.matchTemplate(img,template,cv2.TM_CCOEFF)
        right_score+=result[0][0]
    if left_score>right_score:
        print('left')
    else:
        print('right')
    print("left_score:",left_score,';right_score:',right_score)
def img_similarity(img):
    path_left='template/left/5.jpg'
    path_right='template/right/5.jpg'
    img_right=cv2.imread(path_right, cv2.IMREAD_GRAYSCALE)
    img_left=cv2.imread(path_left, cv2.IMREAD_GRAYSCALE)
    w1,h1=img_right.shape
    w2,h2=img_left.shape
    img1=cv2.resize(img_right, (h1, w1))
    img2=cv2.resize(img_left, (h2, w2))
    orb=cv2.ORB_create()
    kp,des=orb.detectAndCompute(img, None)
    kp1,des1=orb.detectAndCompute(img1, None)
    kp2,des2=orb.detectAndCompute(img2, None)
    bf=cv2.BFMatcher(cv2.NORM_HAMMING)
    matches_right=bf.knnMatch(des, trainDescriptors=des1, k=2)
    matches_left=bf.knnMatch(des, trainDescriptors=des2, k=2)
    good_right=[m for (m, n) in matches_right if m.distance < 0.75 * n.distance]
    good_left=[m for (m, n) in matches_left if m.distance < 0.75 * n.distance]
    similary_1=float(len(good_right))/len(matches_right)
    similary_2=float(len(good_left))/len(matches_left)
    '''
    if similary > 0.1:
        print("判断为ture,两张图片相似度为:%s" % similary)
    else:
        print("判断为false,两张图片相似度为:%s" % similary)'''
    if similary_1>similary_2:
        print('right')
    else:
        print('left')
def circle_extract(img,flag):
    img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #img=cv2.equalizeHist(img)
    circles=cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,90,param1=100,param2=70,minRadius=0,maxRadius=60)
    if flag==1:
        if circles is not None:
            for circle in circles[0]:
                x = int(circle[0])
                y = int(circle[1])
                r = int(circle[2])
                draw_circle = cv2.circle(img ,(x,y) ,r ,(255,255,255) ,1,10 ,0)
                cv2.imshow('1',img)
                cv2.waitKey(1)
        else:
            cv2.imshow('1',img)
            cv2.waitKey(1)
    elif flag==0:        
        if circles is None:
            print('no circle')
        elif len(circles[0])>1:
            print("more than one circle")
        else:
            circle=circles[0][0]
            x = int(circle[0])
            y = int(circle[1])
            r = int(circle[2])
            if r>0:
                r=int(r/1.414)
                newimg=img[y-r:y+r,x-r:x+r]
            width=200
            height=200
            points=(width, height)
            newimg=cv2.resize(newimg,points,interpolation=cv2.INTER_LINEAR)
            newimg=newimg[20:180,20:180]
            ret2,newimg= cv2.threshold(newimg,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            #print(newimg.shape)
            #img_match(img)
            #img_similarity(newimg)
            #cv2.imwrite('template/right/'+str(count)+'.jpg',newimg)
            return newimg

'''
thread=0
path='left/'
name=os.listdir(path)
index=0
for i in name:
    img=cv2.imread(path+i)
    circle_extract(img)
    index+=1
    if index==30:
        break'''
'''
width=200
height=200
points=(width, height)
newimg=cv2.resize(newimg,points,interpolation=cv2.INTER_LINEAR)
img_match(newimg)'''

