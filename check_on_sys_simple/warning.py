# !/usr/bin/python2.7
#coding:utf-8
import notify2 as pt
def tip1():
    pt.init("nividia@linux")
    bubble_notify=pt.Notification('success', '恭喜你，签到成功！')
    bubble_notify.show()
def tip2():
    pt.init("nividia@linux")
    bubble_notify=pt.Notification('failed', '啊哦，识别失败，请关注我们的公众号进行注册！！')
    bubble_notify.show()
def tip3():
    pt.init("nividia@linux")
    get_error=pt.Notification('Error', 'Please input your name!')
    get_error.show()
def tip4():
    pt.init("nividia@linux")
    get_success=pt.Notification('Success', 'You are registered successfully.')
    get_success.show()
def tip5():
    pt.init("nividia@linux")
    unknown_error=pt.Notification('Error', 'Failed!')
    unknown_error.show()
