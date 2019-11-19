# yinxin46.github.io
这是我们的小组，我啥都不知道 

我可以做到什么呢

我就是个混子啊

我真的不知道应该怎么办啊

我人都傻掉了，在20点29分

我需要力量


import numpy as np
import cv2 as cv
cap = cv.VideoCapture(0)
i = 0
sThre = 100
while(True):
    ret, frame = cap.read()
    if i == 0:
        cv.waitKey(2000)
        i = i + 1
    ret_2, frame_2 = cap.read()
    #gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    cv.imshow('frame_2',frame_2)
    cv.imshow('yuantu',frame)
    
    d_frame = cv.absdiff(frame, frame_2, sThre)
    cv.imshow('d_frame',d_frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()#释放摄像头
cv.destroyAllWindows()#关闭所有图像窗口


