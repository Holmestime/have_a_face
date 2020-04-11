#!usr/bin/python2.7
# coding=utf-8
from __future__ import print_function
from multiprocessing import Process
from multiprocessing import Pool
#import tkMessageBox
from Tkinter import *
from PIL import Image, ImageTk
from YotoFace import *
import numpy as np
import cv2
#import cv2.cv as cv
import time
import threading
import b
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
        self.pic_copy=object()
        self.num = 1
	self.num0=1
	self.tag=True

        # 显示窗体的变量
        self.top = Tk()
	self.top.attributes('-alpha',0.7)
	#w,h=self.top.maxsize()
	#self.top.geometry("{}x{}".format(w,h))
	self.top.geometry("640x480+400+200")
        #self.top.title('Face Recognition Attendance System')
	self.top.title('')

        #添加显示图像的label和frame
        self.left_frame = Frame(master=self.top)
        self.lmain = Label(master=self.left_frame)
        self.lmain.pack(expand=YES,fill=BOTH)
	self.show_vid()
        self.left_frame.grid(row=0, column=0)
        self.show_vid()
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
        if self.num % 20 == 0:  
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
    def register(self):

        # 对图像进行预处理
        p = cv2.cvtColor(np.array(self.pic_copy), cv2.COLOR_RGB2BGR)
        (x, y, w, h) = self.face
        xt = int(x - 0.16 * w)
        yt = int(y - 0.4 * h)
        wt = int(w * 1.32)
        ht = int(h * 1.54)

        roi = p[yt:yt + ht, xt:xt + wt]

        # 用于特征提取的图像
        pri_show = cv2.resize(roi, (192, 224))
        pri = cv2.resize(roi, (96, 112))

        # 用于显示的图像
        img_show = cv2.cvtColor(pri_show, cv2.COLOR_BGR2RGB)
        # 弹出注册窗口
        RegisterWindow(img_show, pri, self.yotoface)

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
    def tip(self):
	    picname="Picture 2.jpg"
    	    picpath="/home/holmes/face/face/face/face-whole/FaceReco-ultimate/FaceReco-ultimate/user_data/register_image"+picname
   	    user_pic=cv2.imread(picpath,cv2.IMREAD_COLOR)
	    #cv2.namedWindow('Congratulations')
	    cv2.imshow('Congratulations',user_pic)
	    k=cv2.waitKey(0)
	    print(k)
	    if k == 1048689:
	        print(111)
	        cv2.destroyWindows('Congratulations')
	    print(111)
class RegisterWindow(Toplevel):
    # 用于显示的图像，用于特征提取的图像
    def __init__(self, roi, _pri, _yotoface):
        self.yotoface = _yotoface
        self.pri = _pri
        # roi表示当前所检测到的人脸的图像

        Toplevel.__init__(self)
        Toplevel.title(self, string="RegisterWindow")
        img = Image.fromarray(roi)
	global img_s
	img_s=_pri
	#img_s = Image.fromarray(np.uinit8(_pri))
	
        ph = ImageTk.PhotoImage(image=img)
        self.ImageFrame = Frame(self)
        self.aImage = Label(self.ImageFrame, image=ph)
        self.aImage.configure(image=ph)
        self.aImage.imgtk = ph
        self.aImage.pack()
        self.ImageFrame.grid(padx=20)

        self.InfoFrame = LabelFrame(self, text='User Info', font=('', 17))
        self.l_user = Label(self.InfoFrame, text='Username:')
        self.l_user.grid(row=0, sticky=W, pady=10, padx=10)

        self.e = StringVar()

        self.e_user = Entry(self.InfoFrame, textvariable=self.e)
        # self.e.set('Input your name here...')
        self.e_user.grid(row=0, column=1, pady=10, padx=10)
        self.InfoFrame.grid(row=1, pady=20, padx=20)

        self.ButtonFrame = Frame(self)
        self.push = Button(self.ButtonFrame, text='Enter', font=('', 13), command=self.get_name)
        self.push.pack()
        self.ButtonFrame.grid(row=2, pady=10)

        self.resizable(False, False)
	self.lmain.after(1,self.recongition)
        # self.top.mainloop()

    def get_name(self):
        e_name = self.e_user.get()
	
        if e_name is '':
            tkMessageBox.showinfo('Error', 'Please input your name!')
        else:
            if self.yotoface.Generate(self.pri, e_name):
		global img_s
		username=open("/home/holmes/face/face/face/face-whole/FaceReco-ultimate/FaceReco-ultimate/user_data/user_name.txt","a")
		username.write(e_name+'\n')
		username.close()
		imagepath="/home/holmes/face/face/face/face-whole/FaceReco-ultimate/FaceReco-ultimate/user_data/user_image/"+e_name+".npy"
		#img_s.save(imagepath,"jpeg")
		np.save(imagepath,img_s)
                tkMessageBox.showinfo('Success', 'You are registered successfully.')
            else:
                tkMessageBox.showinfo('Error', 'Failed!')

        self.destroy()


if __name__ == '__main__':
    # 人脸识别模块
    yotoFace = YotoFace()

    # 主窗体
    main = MainWindows(yotoFace)
