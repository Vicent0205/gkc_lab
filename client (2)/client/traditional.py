import cv2
import numpy as np
import os
def judge(img):
    h,w=img.shape

    img=img[int(h/5):int(4*h/5),int(w/5):int(w*4/5)]
    h,w=img.shape
    # cv2.imshow("img ",img)
    ans=cv2.GaussianBlur(img,(5,5),1)
    thresh,binary=cv2.threshold(ans,0,255,cv2.THRESH_OTSU)
    cv2.imshow("binary ",binary)
    cv2.waitKey(1)
    # cv2.destroyAllWindows()
    col_zeros=[len(np.where(binary[:,i]==0)[0]) for i in range(w)]
    col_zeros=np.array(col_zeros)
    bound1=int(w/3)
    bound2=w-bound1
    left_num=np.sum(col_zeros[:bound1])
    right_num=np.sum(col_zeros[bound2:])
    # print("left_num  "+str(left_num))
    # print("right_num "+str(right_num))
    # return left_num,right_num
    
    if right_num>500 and left_num>500:
        return 1  #crossing
    else:
        return 0   # no crossing 
def test():
    files=os.listdir("./pic/train/other")
    for file in files:
        img=cv2.imread("./pic/train/other/"+file,0)
        if judge(img)==1:
            print("wrong")
        # break

    # img=cv2.imread("./pic/train/left/pic14.jpg",0)
    # judge(img)
    # left_list=[]
    # right_list=[]
    # files=os.listdir("./pic/train/left")
    # for file in files:
    #     img=cv2.imread("./pic/train/left/"+file,0)
    #     left_num,right_num=judge(img)
    #     left_list.append(left_num)
    #     right_list.append(right_num)
    # left_list=np.array(left_list)
    # right_list=np.array(right_list)
    # print("left min "+str(np.min(left_list)))
    # print("right min "+str(np.min(right_list)))
        # break

#test()