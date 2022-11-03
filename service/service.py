import base64
from service.message import MessageService
import time
import traceback
from config.config import Config
from service.message import MessageService
from api import detail_api,list_api
from api.mode import Detail,List
from model.bid_company_log import CompanyLog,CompanyLogDao

class Service(object):
    def __init__(self):
        self.detail = detail_api.get_list()
        self.list = list_api.get_list()
        cld = CompanyLogDao()
        self.add = cld.add

    def send_alarm(self, title, exp, receiver="wujiefeng"):
        message = []
        message.append("【%s】【%s】" % (title, Config.env()))
        message.append("时间：%s" % time.strftime("%Y-%m-%d %H:%M:%S"))
        message.append(exp)
        MessageService.send_text("\n".join(message), receiver)
    def add_log(self,request_time,ren,method):
        cy_log = CompanyLog()
        if ren['error'] !="":
            self.send_alarm("API ERROR",ren['error'])
        cy_log.code = ren['code']
        cy_log.ip = ren['ip']
        cy_log.data = str(ren['data'])
        cy_log.msg = ren['msg']
        cy_log.words = ren['words']
        cy_log.request_time = request_time
        cy_log.create_time = int(time.time())
        cy_log.api_name = ren['data']['type']
        cy_log.type = method
        self.add(cy_log)
    def request_time(self,start):
        return int(float(time.time())*1000) - start
    def get_list_object(self,type):
        for i in self.list:
            if i[0] == type:
                return i
        return None
    #下拉列表查询
    def get_detail(self,method,start,words,ip):
        exp = ''
        detail = Detail()
        detail.ip = ip
        if not words:
            detail.error = "words参数错误"
            ren = detail.bejson(detail)
            self.add_log(self.request_time(start),ren,method)
            return ren
        detail.words = words
        for i in range(0,len(self.detail)):
            detail.error = ""
            detail.type = self.detail[i][0]
            self.d = self.detail[i][1]()
            try:
                detail = self.d.run(words,detail)
            except:
                exp = traceback.format_exc()
                detail.error = exp
                ren = detail.bejson(detail)
                self.add_log(self.request_time(start),ren,method)
                continue
            ren = detail.bejson(detail)
            self.add_log(self.request_time(start),ren,method)
            return ren
        return ren
    #详情页查询
    def get_list(self,method,start,words,ip,type):
        list = List()
        list.ip = ip
        #根据type调用相应api
        self.o = self.get_list_object(type)
        if not self.o:
            list.error = 'type参数错误'
            ren = list.bejson(list)
            self.add_log(self.request_time(start),ren,method)
            return ren
        if not words:
            list.error = 'words参数错误'
            ren = list.bejson(list)
            self.add_log(self.request_time(start),ren,method)
            return ren
        if not words and not type:
            list.error = '需要参数：words,type'
            ren = list.bejson(list)
            self.add_log(self.request_time(start),ren,method)
            return ren
        list.words = words
        list.type = self.o[0]
        self.l = self.o[1]()
        try:
            list = self.l.run(words,list)
        except:
            exp = traceback.format_exc()
            list.error = exp
            ren = list.bejson(list)
            self.add_log(self.request_time(start),ren,method)
            return ren
        ren = list.bejson(list)
        self.add_log(self.request_time(start),ren,method)
        return ren
    def get(self,method,words,ip,type=''):
        start = int(float(time.time())*1000)
        if method == 'detail':
            return self.get_detail(method,start,words,ip)
        elif method == 'list':
            return self.get_list(method,start,words,ip,type)