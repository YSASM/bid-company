import traceback
from base.AESCBC import get_decrypt_data, get_encrypt_data, get_detail_encrypt_data
from base.http_wrapper import HttpWrapper
from api.mode import DetailData,Detail
import json
class api_kanzhunwang_detail(object):
    def get_list(self,key,page,limit):
        iv = "8krUawwVMg9RdHK4"
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        }
        t = {
            "query": key,
            "pageNum": page,
            "limit": limit+1
        }
        b = get_detail_encrypt_data(t, iv)
        params = (
            ('b', b),
            ('kiv', iv),
        )
        code,response = HttpWrapper.get('https://www.kanzhun.com/api_to/search/company_v2.json', headers=headers, params=params)
        if code!='ok':
            return 0,'网络错误'
        result = get_decrypt_data(response.text, iv)
        return 1,result
    def run(self,words,detail,page=1,limit=100):
        code,res = self.get_list(words,page,limit)
        if code == 0:
            detail.error = res
            return detail
        try:
            res = json.loads(res)
        except:
            exp = traceback.format_exc()
            detail.error = exp
            return detail
        detail.count = res['resdata']['totalCount']
        res = res['resdata']['zpCompanyList']
        # self.corporate_representative = '-'
        # self.registered_capita = '-'
        # self.incorporation_date = '='
        back = []
        for r in res:
            data = DetailData()
            data.logo = r['logo']
            data.name = r['companyName']
            data.keyNo = r['encCompanyId']
            data.corporate_representative = r['legal']
            data.registered_capita = r['registFinance']
            data.incorporation_date = r['registTime']
            back.append(data.bejson(data))
        detail.data = back
        return detail