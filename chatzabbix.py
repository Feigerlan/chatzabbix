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
        quit()
        print("已注销")
    
#    elif msg == "检索事件":
#         getevents()

    elif str.isdigit("".join(re.findall(r'查询事件(\d+)',msg))):
         print(msg)
         eventid = "".join(re.findall(r'查询事件(\d+)',msg))
         print(eventid)
         itchat.send('识别到事件id，开始查询事件'+eventid,toUserName = revmsg['FromUserName'])
         getevent(eventid,revmsg['FromUserName'])      
    
    elif str.isdigit("".join(re.findall(r'确认事件(\d+)',msg))):
        eventid = "".join(re.findall(r'确认事件(\d+)',msg))
        #messages = "".join(re.findall(r'确认消息<(.+)>',msg))
        #有确认消息，不关闭问题
        if "".join(re.findall(r'(确认消息)<.+>',msg)) == "确认消息" and "".join(re.findall(r'【关闭】',msg)) == "":
            messages = "".join(re.findall(r'确认消息<(.+)>',msg))
            itchat.send("识别到事件id，开始确认事件"+eventid+"，确认消息为:"+messages,toUserName = revmsg['FromUserName'])
            ackevent(eventid,revmsg['FromUserName'],messages)
        #无确认消息，关闭问题    
        elif "".join(re.findall(r'(确认消息)<.+>',msg)) == "" and "".join(re.findall(r'【关闭】',msg)) == "【关闭】":
            itchat.send("识别到事件id，开始确认事件"+eventid+"，无确认消息。关闭问题。",toUserName = revmsg['FromUserName'])
            ackevent(eventid,revmsg['FromUserName'],action=1)
        #有确认消息，关闭问题
        elif "".join(re.findall(r'(确认消息)<.+>',msg)) == "确认消息" and "".join(re.findall(r'【关闭】',msg)) == "【关闭】":
            messages = "".join(re.findall(r'确认消息<(.+)>',msg))
            itchat.send("识别到事件id，开始确认事件"+eventid+"，确认消息为:"+messages+"。关闭问题。",toUserName = revmsg['FromUserName'])
            ackevent(eventid,revmsg['FromUserName'],messages,1)
        #无确认消息，不关闭问题。
        else:
            print("识别到事件id:"+eventid)
            itchat.send("识别到事件id，开始确认事件:"+eventid,toUserName = revmsg['FromUserName'])
            ackevent(eventid,revmsg['FromUserName'])      
    
    elif msg == "查询告警":
         gettrigger(revmsg['FromUserName'])
         print("查询问题触发器")
         
  #  elif msg == "告警":
  #       gaojing()
  #       print("执行告警")

    else:
        welcome = "您好，欢迎使用zabbix微信告警系统！你可以回复关键字\n(查询告警、确认事件、查询事件等)实现功能\n如：确认事件12345,确认消息<已解决>【关闭】（确认消息以“<>”为分隔符）\n如：查询事件1234\n更多功能正在研发中，敬请期待！"
        itchat.send(welcome,toUserName = revmsg['FromUserName'])
#######################################
#######################################
def quit():
    itchat.logout()
#######################################
def gaojing(fromuser):
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

def gettrigger(fromuser): #获取当前触发器
    auth = authenticate(url, username, password)
    trigerIDs = gettrigetID(url,auth)    #获取触发器列表
    for trigerIDresault in trigerIDs:    #遍历触发器
        eventlist = triggergetevents(trigerIDresault['triggerid'],url,auth)  #获取事件列表
        #for event in eventlist:        #遍历事件
        #   if event['acknowledged'] == '0' and event['value'] == '0':
        #       print(event)
        #       print(event['eventid'])
        #   else:
        #       continue  
    xiaoxi=str(trigerIDs)
    itchat.send(xiaoxi,toUserName = fromuser)

def ackevent(eventid,fromuser,message="已确认(微信默认消息)",action=0):  #确认事件
    auth = authenticate(url, username, password)
    #执行事件确认操作,并返回已确认事件的对象
    eventobj=eventackknowledge(eventid,url,auth,message,action)  #调取确认事件的方法
    if 'eventids' in eventobj: #eventobj这事件ID的字典
        itchat.send(str(eventobj['eventids'])+"事件确认成功",toUserName = fromuser)
    else:
        itchat.send("确认事件失败："+eventobj,toUserName = fromuser)

def getevent(eventid,fromuser):
    auth = authenticate(url, username, password)
    event=eventget(eventid,url,auth)  #查询事件
    itchat.send(str(event),toUserName = fromuser)

def getevents():   #通过时间获取事件
    auth = authenticate(url, username, password)
    users = itchat.search_friends(name=u'Feiger')
    userName = users[0]['UserName']
    events = timegetevents("1523030400","1523116800",url,auth)
    print(events)
    #xiaoxi=str(events[0])
    #itchat.send(xiaoxi,toUserName = userName)
    
#######################################
if __name__ == '__main__':
    itchat.auto_login(enableCmdQR=2)
    itchat.run()
