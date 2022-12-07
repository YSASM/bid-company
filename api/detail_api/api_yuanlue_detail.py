from api.mode import DetailData
from base.get_md5 import get_md5
from model.bid_company import CompanyDao
class api_yuanlue_detail(object):
    def __init__(self):
        self.cd = CompanyDao()
    def run(self,words,detail,**kwarg):
        companys = self.cd.match_detail_companys(words)
        if companys==[]:
            return detail
        back = []
        for item in companys:
            if item.corporate_representative:
                data = DetailData()
                data.logo = item.logo
                data.name = item.name
                data.keyNo = str(item.id)
                data.corporate_representative = item.corporate_representative
                data.registered_capita = item.registered_capital
                data.incorporation_date = item.incorporation_date 
                back.append(data.bejson(data))
        detail.data = back
        return detail
