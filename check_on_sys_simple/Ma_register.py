# coding=utf-8
from __future__ import print_function
from multiprocessing import Process

import tkMessageBox
from Tkinter import *
from PIL import Image, ImageTk
from YotoFace import *
import numpy as np
import cv2
import time
import threading

class Ma_register(object):
    def __init__(self, _img,_id):
	self.img=_img
	self.num = 0
	self.pic_copy=[]
	self.id=_id
	# 人脸检测分类器
        self.faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
	self.face = object()
	self.pri=object()

    def access(self):
        img = cv2.flip(self.img, 1)
	pic=img
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
	print(i)
        if i > 0:
            self.face = (x, y, w, h) = faces[j]
            self.pic_copy = pic.copy()
        else:
	    self.pic_copy=[]

    def register(self):
        # 对图像进行预处理
	if self.pic_copy==[]:
	    print('register failed')
	    return False
        p = cv2.cvtColor(np.array(self.pic_copy), cv2.COLOR_RGB2BGR)
        (x, y, w, h) = self.face
        xt = int(x - 0.16 * w)
        yt = int(y - 0.4 * h)
        wt = int(w * 1.32)
        ht = int(h * 1.54)

        roi = p[yt:yt + ht, xt:xt + wt]

        # 用于特征提取的图像
        self.pri = cv2.resize(roi, (96, 112))
        # 弹出注册窗口
        self.save()
	print('register succeed')
	return True

    def save(self):
	e_name=self.id
	username=open("./user_data/user_name.txt","a")
	username.write(e_name+'\n')
	username.close()
	savepath="./user_data/user_image/"+e_name
	np.save(savepath,self.pri)
        cv2.imshow("camera",self.pri)
        key = cv2.waitKey(0)




if __name__ == '__main__':

    # 主窗体
    picname="Picture 2.jpg"
    picpath="./user_data/register_image/"+picname
    user_pic=cv2.imread(picpath,cv2.IMREAD_COLOR)
    regis = Ma_register(user_pic,"liushi")

    regis.access()
    regis.register()
