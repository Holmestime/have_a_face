# coding=utf-8 
import cv2 
import Tkinter as tk
import time
import threading
import os
class Application(tk.Frame):
    def __init__(self,master=None):
	self.num=0
	tk.Frame.__init__(self,master)
	self.pack()
	self.createWidgets()
    def createWidgets(self):
	self.hi_there=tk.Button(self)
	self.hi_there['text']="Congratulations"
	self.hi_there.pack(side="top")
	global root
	root.after(3000,closewin)
def closewin():
    	global root
        root.destroy()
def run():
        global root
        root=tk.Tk()
        app=Application(master=root)
        #threading.Thread(target=closewin).start()
	#w,h=root.maxsize()
	#root.geometry("{}x{}".format(w,h))
        app.mainloop()
	print(2)
	return True
if __name__ == '__main__':
    run()
