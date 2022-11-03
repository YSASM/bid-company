import traceback
from base.http_wrapper import HttpWrapper
from api.mode import DetailData,Detail
import json
class KanzhunwangDetail(object):
    def get_list(self,key):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        }
        params = (
            ('query', key),
        )
        code,response = HttpWrapper.get('https://www.kanzhun.com/api/search/autoComplete_v3.json', headers=headers, params=params)
        if code!='ok':
            return 0,'网络错误'
        return 1,response.text
    def run(self,words,detail):
        code,res = self.get_list(words)
        if code == 0:
            detail.error = res
            return detail
        try:
            res = json.loads(res)
        except:
            exp = traceback.format_exc()
            detail.error = exp
            return detail
        res = res['resdata']
        back = []
        for r in res:
            data = DetailData()
            data.logo = r['logo']
            data.name = r['value']
            data.keyNo = r['encSearchId']
            back.append(data.bejson(data))
        detail.num = len(back)
        detail.list = back
        return detail