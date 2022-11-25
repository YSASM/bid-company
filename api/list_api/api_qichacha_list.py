import json
import traceback
import requests
from bs4 import BeautifulSoup
from base.http_wrapper import HttpWrapper
from api.mode import ListData
# class ApiError(BaseException):
#     def __init__(self, message):
#         self.message = message

class QichachaList(object):
    def __init__(self):
        QCCSESSID = "1b2a5699837aab626f5804fc42"
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'cookie': f'QCCSESSID={QCCSESSID};',
            'referer': 'https://www.qcc.com/',
        }
    def run(self,words,list_):
        url = 'https://www.qcc.com/firm/%s.html' % words
        code,response = HttpWrapper.get(url, headers=self.headers)
        if code!='ok':
            return json.dumps({'name':'网络错误'})
        html = BeautifulSoup(response.text.replace('\n',''), 'html.parser')
        try:
            trs = html.find('div',class_='cominfo-normal').find_all('tr')
        except:
            if '公司不存在' in response.text:
                return json.dumps({'type':'qichacha','name':'公司不存在'})
            elif'登陆' in response.text:
                return json.dumps({'type':'qichacha','name':'需要登陆'})
            elif'验证码' in response.text:
                return json.dumps({'type':'qichacha','name':'需要验证码'})
            else:
                return json.dumps({'type':'qichacha','name':'未知错误:'+traceback.format_exc()})
        temp = []
        for tr in trs:
            td = tr.find_all('td')
            temp.append(td)
        temp2 = html.find('div',class_='contact-info').find_all('div')
        data = ListData()
        try :
            data.name = temp[0][3].find('div',class_='app-copy-box').text.replace(' ','')
        except:pass
        try :
            data.old_name = temp[0][3].find('div',class_='text-gray').find('span').text.replace(' ','')
        except:pass
        try :
            data.registration_status = temp[1][3].text
        except:pass
        try :
            data.corporate_representative = temp[1][1].find('span',class_='cont').find('span').find('a').text
        except:pass
        try :    
            data.registered_capital = temp[2][1].text.replace(' ','')
        except:pass
        try :
            data.incorporation_date = temp[1][5].text.replace(' ','')
        except:pass
        try :    
            data.approval_date = temp[5][5].text.replace(' ','')
        except:pass
        try :    
            data.area = temp[6][1].text.replace(' ','')
        except:pass
        try :    
            data.phone = temp2[3].find_all('span')[0].find('span').text.replace(' ','')
        except:pass
        try :    
            data.email = temp2[6].find('a').text.replace(' ','')
        except:pass
        try :    
            data.credit_code = temp[0][1].text.replace(' ','')
        except:pass
        try :    
            data.taxpayer_num = temp[3][5].text.replace(' ','')
        except:pass
        try :    
            data.registration_num = temp[3][3].text.replace(' ','')
        except:pass
        try :    
            data.organization_code = temp[3][1].text.replace(' ','')
        except:pass
        try :    
            data.insured_persons = int(temp[5][3].find('span').text.replace(' ',''))
        except:pass
        try :    
            data.enterprise_type = temp[4][1].text.replace(' ','')
        except:pass
        try :    
            data.industry = temp[7][1].text.replace(' ','')
        except:pass
        try :
            data.en_name = temp[7][3].text.split(',')[0].replace(' Co.','')
        except:pass
        try :
            data.web = temp2[3].find_all('span')[6].text.replace(' ','')
        except:pass
        try :
            data.address = temp[8][1].find('a').text.replace(' ','')
        except:pass
        try :
            data.company_range = temp[9][1].text.replace(' ','')
        except:pass
        list_.data = data.bejson(data)
        return list_
        