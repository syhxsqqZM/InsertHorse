#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
##################################################
#qq:316118740
#BLOG:http://hi.baidu.com/alalmn
# Python 操作ini文件
#  刚学写的不好请大家见谅
##################################################
 
IP1=""  #扫描IP
IP2=""   #当前已经扫到的IP
INITXT="IP.ini"  #INI文件名字
 
import ConfigParser
def ini_get():  #读取INI
    try:
        global IP1
        global IP2
        global INITXT
        config = ConfigParser.ConfigParser()
        config.readfp(open(INITXT))
        IP1 = config.get("ipdata","ip1")
        IP2 = config.get("ipdata","ip2")
    except:
        print "读取INI错误"
        ini_add("","")  #写入INI
 
def ini_add(ip1,ip2):  #写入INI
    try:
        global INITXT
        config = ConfigParser.ConfigParser()
        config.add_section("ipdata")# 设置section段及对应的值
        config.set("ipdata","ip1",ip1)
        config.set("ipdata","ip2",ip2)
        config.write(open(INITXT, "w"))# 写入文件
    except:
       print "写入INI错误"
 
def ini_write(ip1,ip2):  #修改INI
    try:
        global INITXT
        config = ConfigParser.ConfigParser()
        config.read(INITXT)
        if not config.has_section("ipdata"):#看是否存在该Section，不存在则创建
            temp = config.add_section("")
        config.set("ipdata","ip1",ip1)
        config.set("ipdata","ip2",ip2)
        config.write(open(INITXT, "r+"))
    except:
        print "修改INI错误"
        ini_add("","")  #写入INI
 
 
#if __name__=='__main__':
##    ini_get()  #读取INI
##    print IP1
##    print IP2
#
##    ini_add("222222222","3333333333333")  #写入INI
##    ini_get()  #读取INI
##    print IP1
##    print IP2
#
#    ini_write("999999999","0000000000")  #修改INI
#    ini_get()  #读取INI
#    print IP1
#    print IP2
