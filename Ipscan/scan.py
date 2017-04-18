#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
####################################################################
##################################################
#qq:316118740
#BLOG:http://hi.baidu.com/alalmn
# Python 扫描IP段  指定端口是否开放
#  刚学写的不好请大家见谅
##################################################
import socket
import threading,time
socket.setdefaulttimeout(10)  #设置了全局默认超时时间
#查看IP端口是否开放
class socket_port(threading.Thread):
    def __init__(self,cond, name):
        super(socket_port, self).__init__()
        self.cond = cond
        self.cond.set()#将标识位设为Ture
        self.HOST = name
    def run(self):
        #time.sleep(1) #确保先运行Seeker中的方法
        try:
            PORT=40310
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.HOST,PORT))
            print""
            print self.HOST,u":",PORT,u"端口开放"
            #self.cond.wait()#堵塞线程，直到Event对象内部标识位被设为True或超时（如果提供了参数timeout）。
            self.cond.set()#将标识位设为Ture
            return 1
        except:
            print ".",
            #print self.HOST,u":",PORT,u"端口未开放"
            #self.cond.wait()#堵塞线程，直到Event对象内部标识位被设为True或超时（如果提供了参数timeout）。
            self.cond.set()#将标识位设为Ture
        return 0
##
#socket_port("192.168.2.1")
#if socket_port("192.168.2.100"):
#    print "开放"
#else:
#    print "未开放"
 
def ip2num(ip):
    ip = [int(x) for x in ip.split('.')]
    return ip[0]<<24 | ip[1]<<16 | ip[2]<<8 | ip[3]
 
def num2ip(num):
    #time.sleep(0.05) #50ms
    #time.sleep(0.1) #s
#    data='%s.%s.%s.%s' % (  (num & 0xff000000) >> 24,
#                                 (num & 0x00ff0000) >> 16,
#                                 (num & 0x0000ff00) >> 8,
#                                  num & 0x000000ff  )
#    #socket_port(data)  #查看IP端口是否开放
    if num>=IPend:
        print u"IP导入数组完成"
    return '%s.%s.%s.%s' % (  (num & 0xff000000) >> 24,
                              (num & 0x00ff0000) >> 16,
                              (num & 0x0000ff00) >> 8,
                              num & 0x000000ff  )
 
def gen_ip(ip1,ip2):  #返回数组
#    ip
#    global IPend
#    start, IPend = [ip2num(x) for x in ip.split('-')]
    global IPend
    IPend=ip2
    return [num2ip(num) for num in range(ip1,ip2+1) if num & 0xff]
 
import ini
if __name__=='__main__':
    ini.ini_get()  #读取INI
    list_ip=gen_ip(ip2num(ini.IP1),ip2num(ini.IP2))
    I1 = 0 #得到list的第一个元素
    print u"开始扫描IP"
    ip=0
    while I1 < len(list_ip):
        #print list_ip[I1]
        time.sleep(0.3) #确保先运行Seeker中的方法
        cond = threading.Event()
        hider = socket_port(cond,list_ip[I1])
        hider.start()
        if ip>=255:
            ini.ini_write(list_ip[I1],ini.IP2)  #修改INI
            print ip
            ip=0
        ip=ip+1
        I1 = I1 + 1   #一层
