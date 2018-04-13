#coding=utf-8
import urllib.request, urllib.error, urllib.parse
import sys
import json
import argparse
from login import *
from function import *
########################################################################

import itchat
import time
import re
import requests
import threading
import shutil
import os

'''
reload(sys)
sys.setdefaultencoding('utf-8')
'''
self_name='PH'

 
@itchat.msg_register(itchat.content.TEXT)
def cmd(revmsg):
    msg = revmsg['Text']
    if msg == "注销登录":
        itchat.send('正在注销登录...已注销',toUserName = revmsg['FromUserName'])
        quit()
        print("已注销")
    elif msg == "确认告警":
         #itchat.send('请输入事件ID',toUserName = revmsg['FromUserName'])
         ackalert(revmsg['FromUserName'])
    elif msg == "检索事件":
         getevents()
    elif str.isdigit("".join(re.findall(r'确认事件：(\d+)',msg))):
         itchat.send('识别到事件ID，开始确认事件！',toUserName = revmsg['FromUserName'])
         ackevent(msg,revmsg['FromUserName'])      
    elif msg == "触发器":
         gettrigger()
         print("查询触发器")
    elif msg == "告警":
         gaojing()
         print("执行告警")
    else:
     welcome = "您好，欢迎使用zabbix微信告警系统！你可以回复关键字(查询告警、确认事件、触发器、告警等)实现功能\n更多功能正在研发中，敬请期待！"
     itchat.send('正在注销登录...已注销',toUserName = revmsg['FromUserName'])
#######################################
#######################################
def quit():
    itchat.logout()
#######################################
def gaojing():
    users = itchat.search_friends(name=u'Feiger')
    userName = users[0]['UserName']
    #登陆zabbix获取auth
    auth = authenticate(url, username, password)
    #状态0是启用监控，1是禁用监控
    status=1
    #定义操作ip
    hostip='192.168.15.139'
    #通过hostip获取zabbix 
    hostids=ipgetHostsid(hostip,url,auth)
    hostid=hostids[0]['hostid']
    alerts=actionidgetalert(url,auth)
    xiaoxi=str(alerts[0])
    itchat.send(xiaoxi,toUserName = userName)
def gettrigger(): #获取当前触发器
    auth = authenticate(url, username, password)
    users = itchat.search_friends(name=u'Feiger')
    userName = users[0]['UserName']
    trigerIDs = gettrigetID(url,auth)    #获取触发器列表
    for trigerIDresault in trigerIDs:    #遍历触发器
        eventlist = triggergetevents(trigerIDresault['triggerid'],url,auth)  #获取事件列表
        for event in eventlist:        #遍历事件                                      
           if event['acknowledged'] == '0':
               print(event['eventid'])
           else:
               continue  
    xiaoxi=str(trigerIDs)
    itchat.send(xiaoxi,toUserName = userName)
def ackevent(msg,fromuser):  #确认事件
    auth = authenticate(url, username, password)
    #执行事件确认操作,并返回已确认事件的对象
    eventobj=eventackknowledge(msg,url,auth)  #调取确认事件的方法
    if 'eventids' in eventobj:
        itchat.send(eventobj['eventids']+"事件确认成功",toUserName = userName)
    else:
        itchat.send(eventobj,toUserName = fromuser)
def getevents():   #通过时间获取事件
    auth = authenticate(url, username, password)
    users = itchat.search_friends(name=u'Feiger')
    userName = users[0]['UserName']
    events = timegetevents("1523030400","1523116800",url,auth)
    print(events)
    #xiaoxi=str(events[0])
    #itchat.send(xiaoxi,toUserName = userName)
def ackalert(fromuser):  
    itchat.send('请输入事件ID格式（例如：确认事件：12345）',toUserName = fromuser)
    
#######################################
if __name__ == '__main__':
    itchat.auto_login(enableCmdQR=2)
    itchat.run()
