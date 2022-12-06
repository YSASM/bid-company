import json
import re
import traceback
from base.tools import tool
from base.http_wrapper import HttpWrapper
from api.mode import Detail,DetailData

# 输入关键词，获取下拉菜单
QCCSESSID = "1b2a5699837aab626f5804fc42"
class api_qichacha_detail(object):
    def get_tid(self):
        headers = {
            'cookie': f'QCCSESSID={QCCSESSID};',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }

        params = (
            ('key', '\u4E07\u8FBE\u96C6\u56E2'),
        )
        code,response = HttpWrapper.get('https://www.qcc.com/web/search', headers=headers, params=params)
        if code!='ok':
            return 0,'网络错误'
        try:
            result = re.search("window.tid='(.{32})'<", response.text, re.S).group(1)
        except:
            return 0,'返回错误'
        return 1,result
    def run(self,input_key,detail,**kwarg):
        code,tid = self.get_tid()
        if code == 0:
            detail.error = tid
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
        code,res = HttpWrapper.get('https://www.qcc.com/api/search/searchMind', headers=headers, params=params)
        if code!='ok':
            detail.error = '网络错误'
            return detail
        try:
            res = json.loads(res.text)
        except:
            exp = traceback.format_exc()
            detail.error = exp
            return detail
        try:
            res = res['list']
        except:
            exp = traceback.format_exc()
            detail.error = exp
            return detail
        back = []
        for r in res:
            data = DetailData()
            data.logo = r['ImageUrl']
            data.name = r['name']
            data.keyNo = r['KeyNo']
            back.append(data.bejson(data))
        detail.data = back
        return detail