# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\shivanbh\Anaconda3\Lib\site-packages\PyQt5\uic\Resolute.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import detector_object as inf
from PIL import Image
import numpy as np
import os.path
import sys
from tkinter import Tk  

  
from tkinter import messagebox


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.filedialog = QtWidgets.QFileDialog()
        self.fileCount = 0;
        self.files = []
        self.fileitr = 0;
        self.threshold_value = 0.60
        self.picImage = "i2.jpg"
        self.labelName = "NoLabel"
        i=0;
        j=0;
        base_Y_cord = 80
        MainWindow.resize(1543, 806)
        font = QtGui.QFont()
        font.setUnderline(False)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pic = QtWidgets.QLabel(MainWindow)
        self.pic.setGeometry(320, 50, 920, 431)
        
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 380, 121, 31))
        self.label_3.setMaximumSize(QtCore.QSize(121, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("Threshold")
        
        self.sp = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.sp.setGeometry(QtCore.QRect(30, 420, 121, 31))
        self.sp.setMinimum(0.00)
        self.sp.setMaximum(1.00)
        
        self.sp.setSingleStep(0.05)
        self.sp.valueChanged.connect(self.valuechange)
        
    
        j , OpenFolder = self.Buttondraw(MainWindow,"Open Folder",base_Y_cord,j)
        OpenFolder.clicked.connect(lambda:self.whichbtn(OpenFolder))
        j , NextImage = self.Buttondraw(MainWindow,"Next Image",base_Y_cord,j)
        NextImage.clicked.connect(lambda:self.whichbtn(NextImage))
        j , PreviousImage = self.Buttondraw(MainWindow,"Previous Image",base_Y_cord,j)
        PreviousImage.clicked.connect(lambda:self.whichbtn(PreviousImage))
        j , SaveAnnotation = self.Buttondraw(MainWindow,"Save Annotation",base_Y_cord,j)
        SaveAnnotation.clicked.connect(lambda:self.whichbtn(SaveAnnotation))
        
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(1350, 50, 250, 20))
        self.label_1.setMaximumSize(QtCore.QSize(121, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_1.setFont(font)
        self.label_1.setObjectName("Model")
        
        i , FRCNN = self.checkBoxdraw(MainWindow,"FRCNN",base_Y_cord,i)
        print (FRCNN.text())
        FRCNN.stateChanged.connect(lambda:self.btnstate(FRCNN))
        i , MobileNet= self.checkBoxdraw(MainWindow,"MobileNet",base_Y_cord,i)
        MobileNet.stateChanged.connect(lambda:self.btnstate(MobileNet))
        i , SSD= self.checkBoxdraw(MainWindow,"SSD",base_Y_cord,i)
        SSD.stateChanged.connect(lambda:self.btnstate(SSD))
        
        
        i = 190
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1350, 230, 250, 20))
        self.label_2.setMaximumSize(QtCore.QSize(121, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("Label")
        
        i , Person = self.checkBoxdraw(MainWindow,"Person",base_Y_cord,i)
        Person.stateChanged.connect(lambda:self.btnstate(Person))
        i , Laptop = self.checkBoxdraw(MainWindow,"Car",base_Y_cord,i)
        Laptop.stateChanged.connect(lambda:self.btnstate(Laptop))
        i , TV = self.checkBoxdraw(MainWindow,"TV",base_Y_cord,i)
        TV.stateChanged.connect(lambda:self.btnstate(TV))
        i , Chair = self.checkBoxdraw(MainWindow,"Chair",base_Y_cord,i)
        Chair.stateChanged.connect(lambda:self.btnstate(Chair))
        
        
      
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(30, 500, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_6.setFont(font)
        font.setBold(True)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.setStyleSheet("background-color: yellow")
        self.pushButton_6.clicked.connect(lambda:self.whichbtn(self.pushButton_6))
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 643, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar) 

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_1.setText(_translate("MainWindow", "Select Model"))
        
        self.label_2.setText(_translate("MainWindow", "Label Filter"))
        self.label_3.setText(_translate("MainWindow", "Threshold"))
        
        self.pushButton_6.setText(_translate("MainWindow", "DETECT"))
        
    def loadImage(self,MODEL_NAME):
        print (self.threshold_value)
        #use full ABSOLUTE path to the image, not relative
        img = self.picImage
        #MODEL_NAME = 'mask_rcnn_inception_v2_coco_2018_01_28'
        img1 = inf.get_roi_label(img,MODEL_NAME,self.threshold_value, self.labelName)  
        Image.fromarray(img1.astype(np.uint8)).save("real_and_recon.png")
        
        image = QtGui.QImage(QtGui.QImageReader("real_and_recon.png").read())
        #self.Image_label.setPixmap(QtGui.QPixmap(image))
        self.pic.setPixmap(QtGui.QPixmap(image))
        
        
    def checkBoxdraw(self,MainWindow,name,base_cord,i):
        _translate = QtCore.QCoreApplication.translate
        
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(1350, base_cord+i , 130, 50))
        i = i+base_cord/2 
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName(name)
        self.checkBox.setStyleSheet("foreground-color: red")
        self.checkBox.setText(_translate("MainWindow", name))
        return i, self.checkBox
    
    def Buttondraw(self,MainWindow,name,base_cord,j):
        _translate = QtCore.QCoreApplication.translate
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, base_cord+j, 181, 31))
        j = j + base_cord;
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName(name)
        self.pushButton.setText(_translate("MainWindow", name))
        self.pushButton.setStyleSheet("background-color: red")
        return j , self.pushButton
    
    def valuechange(self):
      
      self.threshold_value = self.sp.value()
      print (self.threshold_value)
      
      
      
      
    def btnstate(self,b):
      print (b.text())
      if b.text() == "FRCNN":
         if b.isChecked() == True:
            print (b.text()+" is selected")
            self.MODEL_NAME = 'testdetect'
         else:
            print (b.text()+" is deselected")
				
      if b.text() == "SSD":
         if b.isChecked() == True:
            print (b.text()+" is selected")
            self.MODEL_NAME = 'mask_rcnn_resnet50_atrous_coco_2018_01_28'
         else:
            print (b.text()+" is deselected")
      if b.text() == "MobileNet":
         if b.isChecked() == True:
            print (b.text()+" is selected")
            self.MODEL_NAME = 'mask_rcnn_resnet50_atrous_coco_2018_01_28'
         else:
            print (b.text()+" is deselected")
      if b.text() == "Person":
         if b.isChecked() == True:
            print (b.text()+" is selected")
            self.labelName = "person"
         else:
            print (b.text()+" is deselected")
      if b.text() == "Car":
         if b.isChecked() == True:
            print (b.text()+" is selected")
            self.labelName = "car"
         else:
            print (b.text()+" is deselected")
            
            
    
    def whichbtn(self,b):
      print (b.text())
      if b.text() == "Open Folder":
         if b.isChecked() == True:
            print (b.text()+" is selected")
         else:
            print (b.text()+" is deselected")
            self.openDirDialog()
       
      if b.text() == "Next Image":
         if b.isChecked() == True:
            print (b.text()+" is selected")
         else:
            print (b.text()+" is deselected")
            self.openNextImage()
      if b.text() == "Previous Image":
         if b.isChecked() == True:
            print (b.text()+" is selected")
         else:
            print (b.text()+" is deselected")
            self.openPreviousImage()

            
				
      if b.text() == "DETECT":
         if b.isChecked() == True:
            print (b.text()+" is selected") 
            self.loadImage(self.MODEL_NAME)
         else:
            print (self.MODEL_NAME+" is deselected")
            self.loadImage(self.MODEL_NAME )
    
    def openDirDialog(self):
        dirName = QtWidgets.QFileDialog.getExistingDirectory(
        None, 'Test Dialog', os.getcwd())
        
        for r, d, f in os.walk(dirName):
            for file in f:
                if '.jpg' in file:
                    self.files.append(os.path.join(r, file))
                    self.fileCount = self.fileCount + 1;
        print (self.files[1])
    
    def openNextImage(self):
        self.fileitr = self.fileitr + 1;
        if self.fileitr >= 0 and self.fileitr < self.fileCount:
            
            self.picImage = self.files[self.fileitr]
            
            image = QtGui.QImage(QtGui.QImageReader(self.picImage).read())
            #self.Image_label.setPixmap(QtGui.QPixmap(image))
            self.pic.setPixmap(QtGui.QPixmap(image))
        else:
            self.fileitr = self.fileitr - 1;
            top = Tk()  
            top.geometry("100x100")  
            top.withdraw()
            messagebox.showwarning("warning","No Next Image exist")  
  
             
    def openPreviousImage(self):
        self.fileitr = self.fileitr - 1;
        if self.fileitr >= 0 and self.fileitr < self.fileCount:
            
            self.picImage = self.files[self.fileitr]
            
            image = QtGui.QImage(QtGui.QImageReader(self.picImage).read())
            #self.Image_label.setPixmap(QtGui.QPixmap(image))
            self.pic.setPixmap(QtGui.QPixmap(image))
        else:
            self.fileitr = self.fileitr + 1;
            top = Tk()  
            top.geometry("100x100")  
            top.withdraw()
            messagebox.showwarning("warning","No Previous Image exist")  

        
           
            
            
if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MODEL_NAME = ""
    ui = Ui_MainWindow()
    MainWindow.setStyleSheet("QMainWindow {background: #FFE4C4;}");
    ui.setupUi(MainWindow)
    
    #ui.checkModel(ui.checkBox,MainWindow)
    
    MainWindow.show()
    sys.exit(app.exec_())
