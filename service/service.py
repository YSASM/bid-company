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
from model.bid_company_log import CompanyLog,CompanyLogDao

class Service(object):
    def __init__(self):
        self.detail = detail_api.get_list()
        self.list = list_api.get_list()
        cld = CompanyLogDao()
        self.add = cld.add

    def send_alarm(self, title, exp, receiver=None):
        message = []
        message.append("【%s】【%s】" % (title, Config.env()))
        message.append("时间：%s" % time.strftime("%Y-%m-%d %H:%M:%S"))
        message.append(exp)
        MessageService.send_text("\n".join(message), receiver)
    def add_log(self,request_time,ren,api_name,type):
        cy_log = CompanyLog()
        cy_log.code = ren['code']
        cy_log.ip = ren['ip']
        cy_log.data = str(ren)
        cy_log.request_time = request_time
        cy_log.create_time = int(time.time())
        cy_log.api_name = api_name
        cy_log.type = type
        self.add(cy_log)
    def get(self,method,words,ip):
        exp = ''
        if method == 'detail':
            start = int(float(time.time())*1000)
            for i in self.detail:
                try:
                    self.d = i()
                    data = self.d.run(words)
                except:
                    exp = traceback.format_exc()
                    ren = {'code':1,'ip':ip,'msg':'操作失败。','data':exp}
                    request_time = int(float(time.time())*1000) - start
                    self.add_log(request_time,ren,str(i),'detail')
                    continue
                try:
                    data = json.loads(data)
                except:
                    exp = traceback.format_exc()
                    ren = {'code':1,'ip':ip,'msg':'操作失败。','data':exp}
                    request_time = int(float(time.time())*1000) - start
                    self.add_log(request_time,ren,str(i),'detail')
                    continue
                if data['num']==0:
                    ren = {'code':0,'ip':ip,'msg':'无数据。','data':data}
                else:
                    ren = {'code':0,'ip':ip,'msg':'操作成功。','data':data}
                request_time = int(float(time.time())*1000) - start
                self.add_log(request_time,ren,str(i),'detail')
                return ren
            ren = {'code':1,'ip':ip,'msg':'所有api操作失败。','data':exp}
            request_time = int(float(time.time())*1000) - start
            self.add_log(request_time,ren,str(i),'detail')
            return ren
        elif method == 'list':
            start = int(float(time.time())*1000)
            id = str(int(time.time()))+'#'+ip.replace('.','')
            for i in self.list:
                try:
                    self.d = i()
                    data = self.d.run(words)
                except:
                    exp = traceback.format_exc()
                    ren = {'code':1,'ip':ip,'msg':'操作失败。','data':exp}
                    request_time = int(float(time.time())*1000) - start
                    self.add_log(request_time,ren,str(i),'list')
                    continue
                try:
                    data = json.loads(data)
                except:
                    exp = traceback.format_exc()
                    ren = {'code':1,'ip':ip,'msg':'操作失败。','data':exp}
                    request_time = int(float(time.time())*1000) - start
                    self.add_log(request_time,ren,str(i),'list')
                    continue
                if data['name'] in ['公司不存在','需要验证码','需要登陆'] or '未知错误' in data['name']:
                    ren = {'code':0,'ip':ip,'msg':'无数据。','data':data}
                else:
                    ren = {'code':0,'ip':ip,'msg':'操作成功。','data':data}
                request_time = int(float(time.time())*1000) - start
                self.add_log(request_time,ren,str(i),'list')
                return ren
            ren = {'code':1,'ip':ip,'msg':'所有api操作失败。','data':exp}
            request_time = int(float(time.time())*1000) - start
            self.add_log(request_time,ren,str(i),'list')
            return ren