import cv2 as cv
 
vc = cv.VideoCapture(0)  # 读入视频文件
# vc = cv.VideoCapture("C:/Users/jason/Desktop/152821AA.MP4")
 
rval, firstFrame = vc.read()
firstFrame = cv.resize(firstFrame, (640, 360), interpolation=cv.INTER_CUBIC)
gray_firstFrame = cv.cvtColor(firstFrame, cv.COLOR_BGR2GRAY)   # 灰度化
firstFrame = cv.GaussianBlur(gray_firstFrame, (21, 21), 0)      #高斯模糊，用于去噪
prveFrame = firstFrame.copy()
 
 
#遍历视频的每一帧
while True:
    (ret, frame) = vc.read()
 
    # 如果没有获取到数据，则结束循环
    if not ret:
        break
 
    # 对获取到的数据进行预处理
    frame = cv.resize(frame, (640, 360), interpolation=cv.INTER_CUBIC)
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray_frame = cv.GaussianBlur(gray_frame, (3, 3), 0)
    cv.imshow("current_frame", gray_frame)
    cv.imshow("prveFrame", prveFrame)
 
    # 计算当前帧与上一帧的差别
    frameDiff = cv.absdiff(prveFrame, gray_frame)
    cv.imshow("frameDiff", frameDiff)
    prveFrame = gray_frame.copy()
 
 
    # 忽略较小的差别
    retVal, thresh = cv.threshold(frameDiff, 25, 255, cv.THRESH_BINARY)
 
 
    # 对阈值图像进行填充补洞
    thresh = cv.dilate(thresh, None, iterations=2)
    image, contours, hierarchy = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
 
    text = "Unoccupied"
    # 遍历轮廓
    for contour in contours:
        # if contour is too small, just ignore it
        if cv.contourArea(contour) < 50:   #面积阈值
            continue
 
        # 计算最小外接矩形（非旋转）
        (x, y, w, h) = cv.boundingRect(contour)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied!"
 
    # cv.putText(frame, "Room Status: {}".format(text), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv.putText(frame, "F{}".format(frameCount), (20, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
 
    cv.imshow('frame_with_result', frame)
    cv.imshow('thresh', thresh)
    cv.imshow('frameDiff', frameDiff)
 
    # 处理按键效果
    key = cv.waitKey(60) & 0xff
    if key == 27:  # 按下ESC时，退出
        break
    elif key == ord(' '):  # 按下空格键时，暂停
        cv.waitKey(0)
 
    cv.waitKey(0)
 
