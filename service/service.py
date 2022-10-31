import base64
import json
import logging
import os
import threading
import time
import traceback
from config.config import Config
from service.message import MessageService
from api import detail_api,list_api

class Service(object):
    def __init__(self):
        self.detail = detail_api.get_list()
        self.list = list_api.get_list()

    def send_alarm(self, title, exp, receiver=None):
        message = []
        message.append("【%s】【%s】" % (title, Config.env()))
        message.append("时间：%s" % time.strftime("%Y-%m-%d %H:%M:%S"))
        message.append(exp)
        MessageService.send_text("\n".join(message), receiver)

    def get(self,method,words,ip):
        exp = ''
        if method == 'detail':
            id = str(int(time.time()))+'#'+ip.replace('.','')
            for i in self.detail:
                try:
                    self.d = i()
                    data = self.d.run(words)
                except:
                    exp += traceback.format_exc()
                    exp += ' '
                    continue
                try:
                    data = json.loads(data)
                except:
                    exp += traceback.format_exc()
                    exp += ' '
                    continue
                if exp!="":
                    logging.error(exp)
                return {'code':0,'msg':'操作成功。,id:%s,请求ip：%s'%('0#'+id,ip),'data':data}
            logging.error(exp)
            return {'code':1,'msg':'操作成功。,id:%s,请求ip：%s'%('1#'+id,ip),'data':exp}
        elif method == 'list':
            for i in self.list:
                try:
                    data = i.run(self,words)
                except:
                    exp = traceback.format_exc()
                    # self.send_alarm("Error", exp, Config.get_val('admin', 'jiangyong,jianghuanhuan,wujiefeng'))
                    continue
                if not data:
                    continue
                return {'code':'ok','name':i[0],'data':data}
            return {'code':'error'}