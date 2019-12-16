# !usr/bin/dev/python3
# -*- coding: utf-8 -*-

import socket
import threading
import cv2
from Ma_register import *

def get_photo(sock,userid):
    f = open(r'./user_data/register_image/'+userid+'.jpg', 'wb')
    while True:
        data = sock.recv(8192)
        if data == bytes():
	    print('已关闭文件')
            f.close()
            s.close()
	    picpath="./user_data/register_image/"+userid+'.jpg'
    	    user_pic=cv2.imread(picpath,cv2.IMREAD_COLOR)
            regis = Ma_register(user_pic,userid)
            regis.access()
            result=regis.register()
	    if result==True:
		print('success')
	    else:
		print('failed')
            break
        f.write(data)
    
    print('已接受到图片')

def get_order(sock,addr):
	while True:
		global tag
		order = sock.recv(1024)
		if order.decode('utf-8')=='0':
			tag=True #tag为真表示收到公众号的拍照命令

		if tag==True and order.decode('utf-8')=='1':
			sock.send(b'2')
		if order.decode('utf-8')=='2':
			get_photo(sock,addr)
		if not order or order.decode('utf-8')=='3':
			break
	sock.close()
	print('Connection from %s:%s closed.' % addr)


if __name__ == '__main__':
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 打开socket连接
    s= socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)   #建立本地连接
    
    print('等待公众号命令')
    while True:
        #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 打开socket连接
        s= socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)   #建立本地连接
	s.connect(('139.199.207.155', 9003))
        print('connect succeed')
	userid=s.recv(28)
	print(userid)	
	if userid != b'00000000000000000000000000':
	    get_photo(s,userid)
	else:
	    break
    print('transmit finished')
        
