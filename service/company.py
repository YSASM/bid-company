from model.bid_company import CompanyDao


class CompanyService(object):
    name = {}
    id = {}
    def __init__(self):
        self.companys = CompanyDao.query_all()
        for company in self.companys:
            self.id[int(company.id)] = company
            self.name[str(company.name)] = company
    def get_name(self):
        return self.name