#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import cv2
import numpy as np
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QBrush, QPixmap
import os

face_cascade = cv2.CascadeClassifier('D:\cv2\haarcascade_frontalface_default.xml') # 加载人脸特征库
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('D:/images/异常进入时间：'+ time.strftime('%Y-%m-%d-%H_%M_%S',time.localtime(time.time())) +'.avi',fourcc, 20.0, (640,480))
a=0
class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
 
        # self.face_recong = face.Recognition()
        self.timer_camera = QtCore.QTimer()
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0
        self.set_ui()
        self.slot_init()
        self.__flag_work = 0
        self.x =0
        self.count = 0
 
    def set_ui(self):
 
        self.__layout_main = QtWidgets.QHBoxLayout()
        self.__layout_fun_button = QtWidgets.QVBoxLayout()
        self.__layout_data_show = QtWidgets.QVBoxLayout()
        self.label_print = QtWidgets.QLabel(self)
 
 
        self.button_open_camera = QtWidgets.QPushButton(u'打开相机')
 
        self.button_close = QtWidgets.QPushButton(u'退出')
        self.label_print.setText("<B>异常进入时间：</B>"+ time.strftime('%Y-%m-%d-%H_%M_%S',time.localtime(time.time())) +"<B>!!!</B>")
        self.label_print.hide()
        self.label_print.move(300, 400)
        self.label_print.setFixedSize(300, 150)
        #Button 的颜色修改
        button_color = [self.button_open_camera, self.button_close]
        for i in range(2):
            button_color[i].setStyleSheet("QPushButton{color:black}"
                                          "QPushButton:hover{color:red}"
                                          "QPushButton{background-color:rgb(78,255,255)}"
                                          "QPushButton{border:2px}"
                                          "QPushButton{border-radius:10px}"
                                          "QPushButton{padding:2px 4px}")
 
 
        self.button_open_camera.setMinimumHeight(50)
        self.button_close.setMinimumHeight(50)

        # move()方法移动窗口在屏幕上的位置到x = 300，y = 300坐标。
        self.move(500, 500)
 
        # 信息显示
        self.label_show_camera = QtWidgets.QLabel()
        self.label_move = QtWidgets.QLabel()
        self.label_move.setFixedSize(100, 100)
 
        self.label_show_camera.setFixedSize(641, 481)
        self.label_show_camera.setAutoFillBackground(False)

        self.__layout_fun_button.addWidget(self.button_open_camera)
        self.__layout_fun_button.addWidget(self.button_close)
        self.__layout_fun_button.addWidget(self.label_move)
 
        self.__layout_main.addLayout(self.__layout_fun_button)
        self.__layout_main.addWidget(self.label_show_camera)
 
        self.setLayout(self.__layout_main)
        self.label_move.raise_()
        self.setWindowTitle(u'摄像头')

        '''
        # 设置背景图片
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('background.jpg')))
        self.setPalette(palette1)
        '''
    def setlabel(self):# 定义显示按键处理方法
        self.label_print.show()#显示label        
 
    def slot_init(self):
        self.button_open_camera.clicked.connect(self.button_open_camera_click)
        self.timer_camera.timeout.connect(self.show_camera)
        self.button_close.clicked.connect(self.close)


    def button_open_camera_click(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请检测相机与电脑是否连接正确", buttons=QtWidgets.QMessageBox.Ok,
                                                defaultButton=QtWidgets.QMessageBox.Ok)
            # if msg==QtGui.QMessageBox.Cancel:
            #                     pass
            else:
                self.timer_camera.start(30)
                
                self.button_open_camera.setText(u'关闭相机')
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.label_show_camera.clear()
            self.button_open_camera.setText(u'打开相机')
 
 
    def show_camera(self):
        flag, self.image = self.cap.read()
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY) # 转灰
        faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.15, minNeighbors = 5, minSize = (5, 5)) # 检测人脸
        for(x, y, w, h) in faces:
            cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2) # 用矩形圈出人脸
            #self.label_print.show()
            #cv2.imwrite('D:/images/3.png',self.image)
            out.write(self.image)
            print('异常进入！！！')
            a=1
            if a==1 :
                self.label_print.show()
            a=0
        #cv2.imshow("gray", gray)
        #cv2.imshow("now vedio", self.image)

        # face = self.face_detect.align(self.image)
        # if face:
        #     pass
        show = cv2.resize(self.image, (640, 400))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        # print(show.shape[1], show.shape[0])
        #show.shape[1] = 640, show.shape[0] = 480
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))
        # self.x += 1
        # self.label_move.move(self.x,100)
 
        # if self.x ==320:
        #     self.label_show_camera.raise_()
 
 
    def closeEvent(self, event):
        ok = QtWidgets.QPushButton()
        cacel = QtWidgets.QPushButton()
 
        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u"关闭", u"是否关闭！")
 
        msg.addButton(ok,QtWidgets.QMessageBox.ActionRole)
        msg.addButton(cacel, QtWidgets.QMessageBox.RejectRole)
        ok.setText(u'确定')
        cacel.setText(u'取消')
        # msg.setDetailedText('sdfsdff')
        if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
            event.ignore()
        else:
            #             self.socket_client.send_command(self.socket_client.current_user_command)
            if self.cap.isOpened():
                self.cap.release()
            if self.timer_camera.isActive():
                self.timer_camera.stop()
            event.accept()
 
 
 
if __name__ == "__main__":
    App = QApplication(sys.argv)
    ex = Ui_MainWindow()
    ex.show()
    sys.exit(App.exec_())
