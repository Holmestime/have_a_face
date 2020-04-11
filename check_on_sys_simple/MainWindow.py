#!usr/bin/python2.7
# coding=utf-8
from __future__ import print_function
from multiprocessing import Process
from multiprocessing import Pool

from Tkinter import *
from PIL import Image, ImageTk
from YotoFace import *
import numpy as np
import cv2
import time
import threading
import warning
from multiprocessing import Process


class MainWindows(object):
    def __init__(self, _yotoface):
        # 人脸识别模块
        self.yotoface = _yotoface

        # 人脸检测分类器
        self.faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
        # 为显示图像所预留的空间
        self.last_frame = np.zeros((480, 640, 3), dtype=np.uint8)

        # 打开摄像头
        self.cap = cv2.VideoCapture(0)

        # 临时变量
        self.face = object()
        self.pic_copy = object()
        self.num = 1
	self.num0=1
	self.tag=True

        # 显示窗体的变量
        self.top = Tk()
	self.top.attributes('-alpha',0.7)
	#w,h=self.top.maxsize()
	self.top.geometry("{}x{}".format(1370,480))
	#self.top.geometry("640x480+400+200")
        self.top.title('Face Recognition Attendance System')
	#self.top.title('')

        # 添加显示图像的label和frame
        self.left_frame = Frame(master=self.top)
        self.lmain = Label(master=self.left_frame)
        self.lmain.pack(expand=YES,fill=BOTH)
	self.show_vid()
        self.left_frame.grid(row=0, column=0)
        # self.show_vid()
        self.top.mainloop()

    def show_vid(self):
        if not self.cap.isOpened():
            print("Can't open the camera.")
        flag, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        if flag is None:
            print("Major error!")
        elif flag:
            self.last_frame = frame.copy()

        pic = cv2.cvtColor(self.last_frame, cv2.COLOR_BGR2RGB)
	if self.num0 % 360 == 0:
	    if self.tag is True:
      	        #self.top.iconify()
		#self.top.withdraw()
	        self.tag=False
	    else:
	        #w=self.top.winfo_screenwidth()
	        #h=self.top.winfo_screenheight()
	        #self.top.geometry("%dx%d"%(w,h))
		self.top.update()
	        self.top.deiconify()
	        self.tag=True
        if self.num % 2000 == 0:  
            gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)  # 3
            # Detect faces in the image

            faces = self.faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.15,
                minNeighbors=5,
                minSize=(5, 5),
                flags=cv2.CASCADE_SCALE_IMAGE
            )  # 4

            tmp = 0
            i = 0
            j = 0
            for (x, y, w, h) in faces:
                if w > tmp:
                    tmp = w
                    j = i
                i += 1

            if i > 0:
		self.top.update()
	        self.top.deiconify()
                self.face = (x, y, w, h) = faces[j]
                self.pic_copy = pic.copy()
                cv2.rectangle(pic, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 6
	    else:
	        self.top.withdraw()
		self.pic_copy=[]
	    a=Process(target=self.recognition())
	    a.start()
	    a.join()
        img = Image.fromarray(pic)
        imgtk = ImageTk.PhotoImage(image=img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
	self.num0 += 1
        self.num += 1
        self.lmain.after(50, self.show_vid)
    # 注册
     	
    def recognition(self):
        # 对图像进行预处理
	if self.pic_copy==[]:
	    return 
        p = cv2.cvtColor(np.array(self.pic_copy), cv2.COLOR_RGB2BGR)
        (x, y, w, h) = self.face
        xt = int(x - 0.16 * w)
        yt = int(y - 0.35 * h)
        wt = int(w * 1.32)
        ht = int(h * 1.54)

        roi = p[yt:yt + ht, xt:xt + wt]

        # 用于特征提取的图像
        pri = cv2.resize(roi, (96, 112))
        flag, result = self.yotoface.Recognition(pri)

        if flag:
            print(result)
            print('success')
            b.tip1()
        else:
            print('failed')
            b.tip2()
        return
        

   
if __name__ == '__main__':
    # 人脸识别模块
    yotoFace = YotoFace()

    # 主窗体
    main = MainWindows(yotoFace)

