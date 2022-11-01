import json
import traceback
import requests
from bs4 import BeautifulSoup

# class ApiError(BaseException):
#     def __init__(self, message):
#         self.message = message

class Qichacha_list(object):
    def __init__(self):
        QCCSESSID = "1b2a5699837aab626f5804fc42"
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'cookie': f'QCCSESSID={QCCSESSID};',
            'referer': 'https://www.qcc.com/',
        }
    def run(self,words):
        url = 'https://www.qcc.com/firm/%s.html' % words
        response = requests.get(url, headers=self.headers)
        html = BeautifulSoup(response.text.replace('\n','').replace('复制',''), 'html.parser')
        try:
            trs = html.find('div',class_='cominfo-normal').find_all('tr')
        except:
            if '公司不存在' in response.text:
                return json.dumps({'name':'公司不存在'})
            elif'登陆' in response.text:
                return json.dumps({'name':'需要登陆'})
            elif'验证码' in response.text:
                return json.dumps({'name':'需要验证码'})
            else:
                return json.dumps({'name':'未知错误:'+traceback.format_exc()})
        temp = []
        for tr in trs:
            td = tr.find_all('td')
            temp.append(td)
        temp2 = html.find('div',class_='contact-info').find_all('div')
        try :
            name = temp[0][3].text.replace(' ','')
        except:name = ''
        try :
            registration_status = temp[1][3].text
        except:registration_status = ''
        try :
            corporate_representative = temp[1][1].find('span',class_='cont').find('span').find('a').text
        except:corporate_representative = ''
        try :    
            registered_capital = temp[2][1].text.replace(' ','')
        except:registered_capital = ''
        try :
            incorporation_date = temp[1][5].text.replace(' ','')
        except:incorporation_date = ''
        try :    
            approval_date = temp[5][5].text.replace(' ','')
        except:approval_date = ''
        try :    
            area = temp[6][1].text.replace(' ','')
        except:area = ''
        try :    
            phone = temp2[3].find_all('span')[0].find('span').text.replace(' ','')
        except: phone = ''
        try :    
            email = temp2[6].find('a').text.replace(' ','')
        except:email = ''
        try :    
            credit_code = temp[0][1].text.replace(' ','')
        except:credit_code = ''
        try :    
            taxpayer_num = temp[3][5].text.replace(' ','')
        except:pass
        try :    
            registration_num = temp[3][3].text.replace(' ','')
        except:registration_num = ''
        try :    
            organization_code = temp[3][1].text.replace(' ','')
        except:organization_code = ''
        try :    
            insured_persons = int(temp[5][3].find('span').text.replace(' ',''))
        except:insured_persons = 0
        try :    
            enterprise_type = temp[4][1].text.replace(' ','')
        except:enterprise_type = ''
        try :    
            industry = temp[7][1].text.replace(' ','')
        except:industry = ''
        try :
            en_name = temp[7][3].text.split(',')[0].replace(' Co.','')
        except:en_name = ''
        try :
            web = temp2[3].find_all('span')[6].text.replace(' ','')
        except:web = ''
        try :
            address = temp[8][1].find('a').text.replace(' ','')
        except:address = ''
        try :
            company_range = temp[9][1].text.replace(' ','')
        except:company_range = ''
        data = {
            'name' : name,
            'registration_status' : registration_status,
            'corporate_representative' : corporate_representative,
            'registered_capital' : registered_capital,
            'incorporation_date' : incorporation_date,
            'approval_date' : approval_date,
            'area': area,
            'phone' : phone,
            'email' : email,
            'credit_code' : credit_code,
            'taxpayer_num' : taxpayer_num,
            'registration_num' : registration_num,
            'organization_code' : organization_code,
            'insured_persons' : insured_persons,
            'enterprise_type' : enterprise_type,
            'industry' : industry,
            'en_name' : en_name,
            'web'  : web,
            'address' : address,
            'company_range' : company_range
        }
        return json.dumps(data)
        