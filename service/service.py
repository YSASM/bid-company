import json

import requests,socket
from base.get_md5 import get_md5
from collections import Counter
from model.bid_company import Company, CompanyDao
from service.message import MessageService
import time
import traceback
from config.config import Config
from service.message import MessageService
from api import detail_api,list_api
from api.mode import Detail,List,Log,St_Mode,Xingtu
from model.bid_company_log import CompanyLog,CompanyLogDao
from qqwry import QQwry
from service.xingtu import GetXingtuInfo
from base.ansync_call import async_call
class Service(object):
    def __init__(self):
        # self.reload_detail()
        self.detail = detail_api.get_list()
        self.list = list_api.get_list()
        self.cd = CompanyDao()
        self.cld = CompanyLogDao()
        self.add = self.cld.add
        self.q = QQwry()
        self.q.load_file('base/qqwry.dat')

    def send_alarm(self, title, exp, receiver="wujiefeng"):
        message = []
        message.append("【%s】【%s】" % (title, Config.env()))
        message.append("时间：%s" % time.strftime("%Y-%m-%d %H:%M:%S"))
        message.append(exp)
        MessageService.send_text("\n".join(message), receiver)
    @async_call
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
        cy_log.api_name = ren['type']
        cy_log.type = method
        cy_log.error = ren['error']
        self.add(cy_log)
    def request_time(self,start):
        return int(float(time.time())*1000) - start
    def get_list_object(self,type):
        for i in self.list:
            if i[0] == type:
                return i
        return None
    def exist_detail(self,item):
        md5 = get_md5(item['name'])
        return self.cd.exist(md5)
    def get_company(self,md5):
        company = self.cd.get_by_md5(md5)
        return company
    @async_call
    def set_company(self,company):
        self.cd.update(company)
    @async_call
    def add_company_detail(self,detail):
        for item in detail.data:
            if self.exist_detail(item):
                self.update_company_detail(item)
                continue
            company = Company()
            company.logo = item['logo']
            company.name = item['name']
            company.create_time=int(time.time())
            company.name_md5 = get_md5(item['name'])
            self.cd.add(company)
    @async_call
    def update_company_detail(self,item):
        xm_company = self.get_company(get_md5(item['name']))
        xm_company.logo = item['logo']
        self.set_company(xm_company)
    @async_call
    def update_company_list(self,list):
        xm_company = self.get_company(get_md5(list.data['name']))
        xm_company.registration_status = list.data['registration_status']
        xm_company.corporate_representative=list.data['corporate_representative']
        xm_company.registered_capital=list.data['registered_capital']
        xm_company.incorporation_date=list.data['incorporation_date']
        xm_company.approval_date=list.data['approval_date']
        xm_company.area=list.data['area']
        xm_company.phone=list.data['phone']
        xm_company.email=list.data['email']
        xm_company.credit_code=list.data['credit_code']
        xm_company.taxpayer_num=list.data['taxpayer_num']
        xm_company.registration_num=list.data['registration_num']
        xm_company.organization_code=list.data['organization_code']
        xm_company.insured_persons=list.data['insured_persons']
        xm_company.enterprise_type=list.data['enterprise_type']
        xm_company.industry=list.data['industry']
        xm_company.old_name=list.data['old_name']
        xm_company.en_name=list.data['en_name']
        xm_company.web=list.data['web']
        xm_company.address=list.data['address']
        xm_company.company_range=list.data['company_range']
        self.set_company(xm_company)
    @async_call
    def add_company_list(self,list):
        company = Company()
        # company.logo = list.data['logo']
        company.name = list.data['name']
        company.name_md5 = get_md5(list.data['name'])
        company.registration_status = list.data['registration_status']
        company.corporate_representative=list.data['corporate_representative']
        company.registered_capital=list.data['registered_capital']
        company.incorporation_date=list.data['incorporation_date']
        company.approval_date=list.data['approval_date']
        company.area=list.data['area']
        company.phone=list.data['phone']
        company.email=list.data['email']
        company.credit_code=list.data['credit_code']
        company.taxpayer_num=list.data['taxpayer_num']
        company.registration_num=list.data['registration_num']
        company.organization_code=list.data['organization_code']
        company.insured_persons=list.data['insured_persons']
        company.enterprise_type=list.data['enterprise_type']
        company.industry=list.data['industry']
        company.old_name=list.data['old_name']
        company.en_name=list.data['en_name']
        company.web=list.data['web']
        company.address=list.data['address']
        company.company_range=list.data['company_range']
        company.create_time=int(time.time())
        company.update_time=company.create_time
        self.cd.add(company)
    #下拉列表查询
    def exist_list(self,list):
        md5 = get_md5(list.data['name'])
        return self.cd.exist(md5)

    def get_detail(self,method,start,words,ip,write_log=True,**kwarg):
        exp = ''
        detail = Detail()
        detail.ip = ip
        if not words:
            detail.error = "words参数错误"
            ren = detail.bejson(detail)
            if write_log:
                self.add_log(self.request_time(start),ren,method)
            return ren
        detail.words = words
        for i in self.detail:
            if i[2] == "2":
                continue
            detail.error = ""
            detail.type = i[0]
            self.d = i[1]()
            try:
                detail = self.d.run(words,detail,**kwarg)
            except:
                exp = traceback.format_exc()
                detail.error = exp
                ren = detail.bejson(detail)
                if write_log:
                    self.add_log(self.request_time(start),ren,method)
                continue
            if len(detail.data) == 0:
                continue
            if detail.type!="yuanlue":
                try:
                    self.add_company_detail(detail)
                except:
                    exp = traceback.format_exc()
                    detail.error = exp
                    ren = detail.bejson(detail)
                    if write_log:
                        self.add_log(self.request_time(start),ren,method)
                    return ren
            ren = detail.bejson(detail)
            if write_log:
                self.add_log(self.request_time(start),ren,method)
            return ren
        detail.error = "无结果"
        ren = detail.bejson(detail)
        return ren
    #详情页查询
    def get_list(self,method,start,words,ip,type,write_log=True):
        list = List()
        list.ip = ip
        #根据type调用相应api
        self.o = self.get_list_object(type)
        if not self.o:
            list.error = 'type参数错误'
            ren = list.bejson(list)
            if write_log:
                self.add_log(self.request_time(start),ren,method)
            return ren
        if not words:
            list.error = 'words参数错误'
            ren = list.bejson(list)
            if write_log:
                self.add_log(self.request_time(start),ren,method)
            return ren
        if not words and not type:
            list.error = '需要参数：words,type'
            ren = list.bejson(list)
            if write_log:
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
            if write_log:
                self.add_log(self.request_time(start),ren,method)
            return ren
        try:
            if list.type!="yuanlue":
                if not self.exist_list(list):
                    self.add_company_list(list)
                else:
                    self.update_company_list(list)
        except Exception as e:
            self.send_alarm('get_list','add sql error:'+str(e))
        ren = list.bejson(list)
        if write_log:
            self.add_log(self.request_time(start),ren,method)
        return ren
    def get(self,method,words,ip,start,type='',**kwarg):
        if method == 'detail':
            self.reload_d()
            return self.get_detail(method,start,words,ip,**kwarg)
        elif method == 'list':
            return self.get_list(method,start,words,ip,type)
    def get_log_byId(self,id):
        try:
            backlog = Log()
            log = self.cld.get_by_id(id)
            backlog.logs = [self.cld.bejson(log)]
        except:
            exp = traceback.format_exc()
            self.send_alarm('get_log_byId',exp)
            backlog.error = exp
        ren = backlog.bejson(backlog)
        return ren
    def get_log_byTime(self,start,end):
        backlog = Log()
        try:
            logs = self.cld.get_by_time(start,end)
            back = []
            for log in logs:
                back.append(self.cld.bejson(log))
            backlog.logs = back
        except:
            exp = traceback.format_exc()
            self.send_alarm('get_log_byTime',exp)
            backlog.error = exp
        ren = backlog.bejson(backlog)
        return ren
    def get_log_byWords(self,words):
        try:
            backlog = Log()
            logs = self.cld.get_by_words(words)
            back = []
            for log in logs:
                back.append(self.cld.bejson(log))
            backlog.logs = back
        except:
            exp = traceback.format_exc()
            self.send_alarm('get_log_byWords',exp)
            backlog.error = exp
        ren = backlog.bejson(backlog)
        return ren
    def get_logs(self):
        backlog = Log()
        try:
            logs = self.cld.query_all()
            back = []
            for log in logs:
                back.append(self.cld.bejson(log))
            backlog.logs = back
        except:
            exp = traceback.format_exc()
            self.send_alarm('get_logs',exp)
            backlog.error = exp
        ren = backlog.bejson(backlog)
        return ren
    def st_error(self,start,end):
        back = St_Mode()
        try:
            logs = self.cld.st_error(start,end)
            for log in logs:
                back.data.append(self.cld.bejson2(log))         
        except:
            exp = traceback.format_exc()
            self.send_alarm('st_error',exp)
            back.error = exp
        ren = back.bejson(back)
        return ren
    def st_words(self,start,end):
        # http://www.inte.net/tool/ip/api.ashx?ip=183.136.213.98&datatype=json
        back = St_Mode()
        try:
            logs = self.cld.st_words(start,end)
            wdlist=[]
            for log in logs:
                if log.words == '':
                    continue
                wdlist.append(log.words)
            words = Counter(wdlist)
            for word in words:
                back.data.append({'words':word,'times':words[word]})
                back.data.sort(key = lambda i:i['times'],reverse=True)
        except:
            exp = traceback.format_exc()
            self.send_alarm('st_words',exp)
            back.error = exp
        ren = back.bejson(back)
        return ren
    def check_ip(self,argv):
        try:
            result = self.q.lookup(argv)
        except:
            self.send_alarm('st_address','ip match error.\nip:'+argv)
            return '其他'
        if not result:
            return '其他'
        result,x=result
        return result
    def st_address(self,start,end):
        back = St_Mode()
        try:
            logs = self.cld.get_by_time(start,end)
            address = []
            for log in logs:
                ip = log.ip
                # ip = '110.41.14.33'
                if ip == '127.0.0.1':
                    where = '本地访问'
                elif ip == '':
                    continue
                else:
                    where = self.check_ip(ip)
                address.append(where)
            address = Counter(address)
            for a in address:
                back.data.append({'words':a,'times':address[a]})
                back.data.sort(key = lambda i:i['times'],reverse=True)
        except:
            exp = traceback.format_exc()
            self.send_alarm('st_address',exp)
            back.error = exp
        ren = back.bejson(back)
        return ren
    def st_time(self,start,end):
        back = St_Mode()
        try:
            logs = self.cld.get_by_time(start,end)
            retimes={
                'list':[],
                'detail':[]
            }
            for log in logs:
                if log.type=='list':
                    retimes['list'].append(log.request_time)
                elif log.type=='detail':
                    retimes['detail'].append(log.request_time)
            retimes['list'] = sum(retimes['list'])/len(retimes['list']) if retimes['list']!=[] else 0
            retimes['detail'] = sum(retimes['detail'])/len(retimes['detail']) if retimes['detail']!=[] else 0
            retimes['list'] = str(int(retimes['list']))+'ms'
            retimes['detail'] = str(int(retimes['detail']))+'ms'
            back.data=[] if retimes['list']=='0ms' and retimes['detail'] == '0ms' else [{
                        'name':'list',
                        'request_time':retimes['list']
                    },
                    {
                        'name':'detail',
                        'request_time':retimes['detail']
                    }]
        except:
            exp = traceback.format_exc()
            self.send_alarm('st_time',exp)
            back.error = exp
        ren = back.bejson(back)
        return ren
    def reload_d(self):
        self.detail = detail_api.get_list()
    def restatus(self,name,status):
        try:
            f = open('base/on_off.json','r')
            old = json.load(f)
            for i in old['data']:
                if i['name']==name:
                    old['data'][old['data'].index(i)]['status']=status
                    break
            f.close()
            f = open('base/on_off.json','w')
            f.write(json.dumps(old))
            f.close()
            return "操作成功",200
        except Exception as e:
            return str(e),500
    def get_yuanlue_api_company_id(self,words):
        yuanlue_detail = detail_api.yuanlue()()
        detail = Detail()
        detail = yuanlue_detail.run(words,detail)
        data = detail.data
        if data == []:
            return {"keyNo":None,"logo":"","name":words}
        return data[0]
    def get_id(self,words,ip):
        data = self.get_yuanlue_api_company_id(words)
        if data["keyNo"]:
            return data
        start = int(float(time.time())*1000)
        detail = self.get_detail('detail',start,words,ip,write_log=False)
        # logging.info(str(detail))
        if detail['data']:
            d = detail['data'][0]
            start = int(float(time.time())*1000)
            self.get_list('list',start,d['keyNo'],ip,detail['type'],write_log=False)
        count = 10
        while not data["keyNo"]:
            if count <= 0:
                break
            data = self.get_yuanlue_api_company_id(words)
            count-=1
            time.sleep(1)
        return data
    def get_xingtu(self,words,ip):
        xingtu = Xingtu()
        xingtu.words = words
        get_xt = GetXingtuInfo()
        try:
            xingtu.ip = ip
            xingtu = get_xt.get(words,xingtu)
        except:
            exp = traceback.format_exc()
            xingtu.error = exp
        xingtu = xingtu.bejson(xingtu)
        return xingtu
    def get_xingtu_simple(self,words,ip):
        xingtu = Xingtu()
        xingtu.words = words
        get_xt = GetXingtuInfo()
        try:
            xingtu.ip = ip
            xingtu = get_xt.GetSearch(words,xingtu)
        except:
            exp = traceback.format_exc()
            xingtu.error = exp
        xingtu = xingtu.bejson(xingtu)
        return xingtu
