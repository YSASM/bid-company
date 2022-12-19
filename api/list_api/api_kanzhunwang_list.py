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
            return 0,'无公司信息或网络错误'
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
        
    def run(self,words,list_):
        code,res = self.info(words)
        if code == 0:
            list_.error = res
            return list_
        code,html = self.html(words)
        if code == 0:
            list_.error = res
            return list_
        try:
            res = json.loads(res)
            res = res['resdata']
        except:
            pass
        data = ListData()
        try:
            if html.find('div',class_='business-container').find('div',class_='item-title').text == '公司全称':
                data.name = html.find('div',class_='business-container').find('div',class_='item-content').text
            else:
                data.name = html.find('h1',class_='base-title').text
        except:
            list_.error = '获取公司名失败'
        try:
            data.logo = html.find('div',class_='logo').find('img').get('src')
        except:
            pass
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
        try:
            data.registration_status = res['registerVO']['manageStatus']
        except:
            pass
        try:
            data.corporate_representative = res['registerVO']['legalPersonName']
        except:
            pass
        try:
            data.registered_capital = res['registerVO']['registerMoney']
        except:
            pass
        try:
            data.incorporation_date = res['registerVO']['createDate']
        except:
            pass
        try:
            data.approval_date = res['registerVO']['checkDate']
        except:
            pass
        try:
            data.area = res['registerVO']['area']
        except:
            pass
        try:
            data.credit_code = res['registerVO']['socialCode']
        except:
            pass
        try:
            data.taxpayer_num = res['registerVO']['taxpayerIdentity']
        except:
            pass
        try:
            data.registration_num = res['registerVO']['registerNumber']
        except:
            pass
        try:
            data.organization_code = res['registerVO']['organizationCode']
        except:
            pass
        try:
            data.insured_persons = int(res['registerVO']['insuredCount'])
        except:
            pass
        try:
            data.enterprise_type = res['registerVO']['companyType']
        except:
            pass
        try:
            data.industry = res['registerVO']['industry']
        except:
            pass
        try:
            data.address = res['registerVO']['registerAddress']
        except:
            pass
        try:
            data.company_range = res['registerVO']['manageScope']
        except:
            pass
        try:
            list_.data = data.bejson(data)
        except:
            pass
        return list_