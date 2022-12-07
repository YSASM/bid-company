from api.mode import DetailData
from base.get_md5 import get_md5
from service.company import CompanyService
class api_yuanlue_detail(object):
    def __init__(self):
        self.cs = CompanyService()
    def run(self,words,detail,**kwarg):
        companys = self.cs.match_detail_companys(words)
        if companys==[]:
            return detail
        back = []
        for item in companys:
            if item.corporate_representative:
                data = DetailData()
                data.logo = item.logo
                data.name = item.name
                data.keyNo = item.id
                data.corporate_representative = item.corporate_representative
                data.registered_capita = item.registered_capital
                data.incorporation_date = item.incorporation_date 
                back.append(data.bejson(data))
        detail.data = back
        return detail
