from sqlalchemy import Column
from sqlalchemy.types import *  # 所有字段类型
from . import DBSession
from . import Base


class Company(Base):
    __tablename__ = "bid_company"  # 数据表的名字
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    registration_status = Column(String(255))
    corporate_representative = Column(String(255))
    registered_capital = Column(String(255))
    incorporation_date = Column(String(255))
    approval_date = Column(String(255))
    province = Column(String(255))
    city = Column(String(255))
    area  = Column(String(255))
    phone = Column(String(255))
    phone_more = Column(String(255))
    email = Column(String(255))
    email_more = Column(String(255))
    credit_code = Column(String(255))
    taxpayer_num = Column(String(255))
    registration_num = Column(String(255))
    organization_code = Column(String(255))
    insured_persons = Column(Integer)
    enterprise_type = Column(String(255))
    industry = Column(String(255))
    old_name = Column(String(255))
    en_name = Column(String(255))
    web  = Column(String(255))
    address = Column(String(255))
    last_address = Column(String(255))
    company_range = Column(Text)
    status = Column(Integer)
    create_time = Column(Integer)
    update_time = Column(Integer)
    
    def __init__(self):
        self.id = 0
        self.name = ""
        self.registration_status = ""
        self.corporate_representative = ""
        self.registered_capital = ""
        self.incorporation_date = ""
        self.approval_date = ""
        self.province = ""
        self.city = ""
        self.area  = ""
        self.phone = ""
        self.phone_more = ""
        self.email = ""
        self.email_more = ""
        self.credit_code = ""
        self.taxpayer_num = ""
        self.registration_num = ""
        self.organization_code = ""
        self.insured_persons = 0
        self.enterprise_type = ""
        self.industry = ""
        self.old_name = ""
        self.en_name = ""
        self.web  = ""
        self.address = ""
        self.last_address = ""
        self.company_range = ""
        self.status = 0
        self.create_time = 0
        self.update_time = 0
class CompanyDao(object):
    def __init__(self):
        self.db = DBSession()

    def __del__(self):
        self.db.close()

    def add(self, company):
        sesion = DBSession()
        sesion.add(company)
        sesion.commit()
        sesion.close()

    def exist(self, name):
        sesion = DBSession()
        res = sesion.query(Company).filter_by(name=name).all()
        sesion.close()
        return len(res) >= 1

    @classmethod
    def query_all(cls):
        session = DBSession()
        o = session.query(Company).all()
        session.close()
        return o