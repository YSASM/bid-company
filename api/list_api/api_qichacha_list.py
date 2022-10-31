import json
import requests
from bs4 import BeautifulSoup

class ApiError(BaseException):
    def __init__(self, message):
        self.message = message

class Qichacha_list(object):
    def __init__(self):
        QCCSESSID = "7e65dea622d446795c386f8c0b"
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'cookie': f'QCCSESSID={QCCSESSID};',
        }
    def run(self,words):
        url = 'https://www.qcc.com/firm/%s.html' % words
        response = requests.get(url, headers=self.headers)
        html = BeautifulSoup(response.text.replace('\n','').replace('复制',''), 'html.parser')
        try:
            trs = html.find('div',class_='cominfo-normal').find_all('tr')
        except:
            raise ApiError('需要验证码！')
        temp = []
        for tr in trs:
            td = tr.find_all('td')
            temp.append(td)
        temp2 = html.find('div',class_='contact-info').find_all('div')
        data = {
            'name' : temp[0][3].text.replace(' ',''),
            'registration_status' : temp[1][3].text,
            'corporate_representative' : temp[1][1].find('span',class_='cont').find('span').find('a').text,
            'registered_capital' : temp[2][1].text.replace(' ',''),
            'incorporation_date' : temp[1][5].text.replace(' ',''),
            'approval_date' : temp[5][5].text.replace(' ',''),
            'area':temp[6][1].text.replace(' ',''),
            'phone' : temp2[3].find_all('span')[0].find('span').text.replace(' ',''),
            'email' : temp2[5].text.replace(' ',''),
            'credit_code' : temp[0][1].text.replace(' ',''),
            'taxpayer_num' : temp[3][5].text.replace(' ',''),
            'registration_num' : temp[3][3].text.replace(' ',''),
            'organization_code' : temp[3][1].text.replace(' ',''),
            'insured_persons' : int(temp[5][3].find('span').text.replace(' ','')),
            'enterprise_type' : temp[4][1].text.replace(' ',''),
            'industry' : temp[7][1].text.replace(' ',''),
            'en_name' : temp[7][3].text.split(',')[0].replace(' Co.',''),
            'web'  : temp2[4].find_all('span')[1].find('span',class_='val').text.replace(' ',''),
            'address' : temp2[7].text.replace(' ','').replace('附近企业',''),
            'company_range' : temp[9][1].text.replace(' ','')
        }
        return json.dumps(data)
        