from cProfile import run
import json
import re
import time
import requests
from api.detail_api.qichacha.tools import tool


# 输入关键词，获取下拉菜单
QCCSESSID = "1b2a5699837aab626f5804fc42"
class Qichacha_Detail(object):
    def __init__(self) -> None:
        self.tid = self.get_tid()
    def get_tid(self):
        
        headers = {
            'cookie': f'QCCSESSID={QCCSESSID};',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }

        params = (
            ('key', '\u4E07\u8FBE\u96C6\u56E2'),
        )
        response = requests.get('https://www.qcc.com/web/search', headers=headers, params=params, verify=False)
        result = re.search("window.tid='(.{32})'<", response.text, re.S).group(1)
        return result
    def run(self,input_key,times=3):
        tid = self.tid
        # tid = '2014a293fa94a9abcee7ce755c00134c'
        header_key = tool.get_key(input_key)
        header_value = tool.get_value(input_key,tid )
        headers = {
            f'{header_key}': f'{header_value}',
            'cookie': f'QCCSESSID={QCCSESSID};',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        }

        params = (
            ('mindKeyWords', 'true'),
            ('mindType', '9'),
            ('pageSize', '5'),
            ('person', 'true'),
            ('searchKey', f'{input_key}'),
            ('suggest', 'true'),
        )
        response = requests.get('https://www.qcc.com/api/search/searchMind', headers=headers, params=params)
        try:
            response = json.loads(response.text)
        except:
            if times == 0:
                return json.dumps(response = {'num':0,'list':'Api失效'})
            self.tid = self.get_tid()
            self.run(input_key,times=times-1)
        try:
            response = response['list']
            response = {'num':len(response),'list':response}
        except:
            response = {'num':0,'list':None}
        return json.dumps(response)
