from model.bid_company import CompanyDao
from api.mode import ListData
class YuanlueList(object):
    def __init__(self):
        self.cd = CompanyDao()
    def run(self,words,list_):
        company = self.cd.get_by_id(words)
        data = ListData()
        data.logo = company.logo
        data.name = company.name
        data.old_name = company.old_name
        data.registration_status = company.registration_status
        data.corporate_representative = company.corporate_representative
        data.registered_capital = company.registered_capital
        data.incorporation_date = company.incorporation_date
        data.approval_date = company.approval_date
        data.area = company.area
        data.phone = company.phone
        data.email = company.email
        data.credit_code = company.credit_code
        data.taxpayer_num = company.taxpayer_num
        data.registration_num = company.registration_num
        data.organization_code = company.organization_code
        data.insured_persons = company.insured_persons
        data.enterprise_type = company.enterprise_type
        data.industry = company.industry 
        data.en_name = company.en_name
        data.web = company.web
        data.address = company.address
        data.company_range = company.company_range
        list_.data = data.bejson(data)
        return list_