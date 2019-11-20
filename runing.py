import sys, cv2, time

from x import Ui_TabWidget

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QFileDialog,QTabWidget 

from PyQt5.QtCore import QTimer, QThread, pyqtSignal, Qt

from PyQt5.QtGui import QPixmap, QImage

from PyQt5.QtWidgets import QLabel,QWidget


class mywindow(QTabWidget,Ui_TabWidget):

    def __init__(self):
        super(mywindow,self).__init__()
        self.setupUi(self)

    def videoprocessing(self):
        print("gogo")
        global videoName 
        videoName,videoType= QFileDialog.getOpenFileName(self,
                                   "D:\images",
                                    "",
                                    "Text Files (test.mp4);;All Files (*)")
        
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()

    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))
    def imageprocessing(self):
        print("hehe")
        imgName,imgType= QFileDialog.getOpenFileName(self,
                                    "D:\images\1.jpg",
                                    "",
                                    "Text Files (test1.png);;All Files (*)")

        print(str(imgName))
        png = QtGui.QPixmap(imgName).scaled(self.label_2.width(), self.label_2.height())
        self.label_2.setPixmap(png)

class Thread(QThread):

    changePixmap = pyqtSignal(QtGui.QImage)
    def run(self):
        cap = cv2.VideoCapture(videoName)
        print(videoName)
        while (cap.isOpened()==True):
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)#在这里可以对每帧图像进行处理，
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                time.sleep(0.01) 
            else:
                break

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())
