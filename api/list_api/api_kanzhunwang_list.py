from base.AESCBC import get_decrypt_data,get_encrypt_data
from base.http_wrapper import HttpWrapper
from api.mode import ListData
from bs4 import BeautifulSoup
import json
class KanzhunwangList(object):
    def info(self,key_no):
        iv = "8krUawwVMg9RdHK4"
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        }
        input_key = key_no

        b = get_encrypt_data(input_key, iv)
        params = (
            ('b', b),
            ('kiv', iv),
        )
        code,response = HttpWrapper.get('https://www.kanzhun.com/api_to/cbi/base_info.json', headers=headers, params=params)
        if code != 'ok':
            return 0,'网络错误'
        result = get_decrypt_data(response.text, iv)
        return 1,result
    def html(self,key_no):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
        }
        code,response = HttpWrapper.get('https://www.kanzhun.com/firm/industry/%s.html' % key_no, headers=headers)
        if code != 'ok':
            return 0,'网络错误'
        html = BeautifulSoup(response.text, 'html.parser')
        return 1,html
        
    def run(self,words,list):
        code,res = self.info(words)
        if code == 0:
            list.error = res
            return list
        code,html = self.html(words)
        if code == 0:
            list.error = res
            return list
        try:
            res = json.loads(res)
            res = res['resdata']
        except:
            pass
        data = ListData()
        try:
            data.name = html.find('h1',class_='base-title').get('title')
        except:
            list.error = '获取公司名失败'
        try:
            cons = html.find('div',class_='text-wrap').find_all('p')
            phone = []
            email = []
            for con in cons:
                con = con.text
                if '@' in con:
                    email.append(con)
                else:
                    phone.append(con)
            data.phone = ','.join(phone)
            data.email = '.'.join(email)
            if data.email == "":
                data.email = "-"
            if data.phone == "":
                data.phone = "-"
        except:
            pass
        try:
            data.old_name = ','.join(res['registerVO']['usedNameList'])
            if data.old_name == "":
                data.old_name = "-"
        except:
            pass
        data.registration_status = res['registerVO']['manageStatus']
        data.corporate_representative = res['registerVO']['legalPersonName']
        data.registered_capital = res['registerVO']['registerMoney']
        data.incorporation_date = res['registerVO']['createDate']
        data.approval_date = res['registerVO']['checkDate']
        data.area = res['registerVO']['area']
        data.credit_code = res['registerVO']['socialCode']
        data.taxpayer_num = res['registerVO']['taxpayerIdentity']
        data.registration_num = res['registerVO']['registerNumber']
        data.organization_code = res['registerVO']['organizationCode']
        data.insured_persons = res['registerVO']['insuredCount']
        data.enterprise_type = res['registerVO']['companyType']
        data.industry = res['registerVO']['industry']
        data.address = res['registerVO']['registerAddress']
        data.company_range = res['registerVO']['manageScope']
        list.content = data.bejson(data)
        return list