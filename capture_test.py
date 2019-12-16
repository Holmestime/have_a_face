# coding=utf-8
from __future__ import print_function

import tkMessageBox
from Tkinter import *
from PIL import Image, ImageTk
from YotoFace import *
import numpy as np
import cv2
import time
import threading

cap=cv2.VideoCapture(0)
while(1):
    ret,frame=cap.read()
    cv2.imshow('capture',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyWindow('capture')

