from api.mode import DetailData
from base.get_md5 import get_md5
from service.company import CompanyService
class api_yuanlue_detail(object):
    def __init__(self):
        self.cs = CompanyService()
    def run(self,words,detail):
        companys = self.cs.match_detail_companys(words)
        if companys==[]:
            return detail
        back = []
        for (id,name,logo,corporate_representative) in companys:
            if corporate_representative:
                data = DetailData()
                data.logo = logo
                data.name = name
                data.keyNo = id
                back.append(data.bejson(data))
        detail.data = back
        return detail
