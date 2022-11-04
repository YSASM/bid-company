import time
from sqlalchemy import Column
from sqlalchemy.types import *
from . import DBSession
from . import Base


class Company(Base):
    __tablename__ = "bid_company"  # 数据表的名字
    id = Column(Integer, primary_key=True)
    logo = Column(String(255))
    name = Column(String(255))
    name_md5 = Column(String(255))
    registration_status = Column(String(255))
    corporate_representative = Column(String(255))
    registered_capital = Column(String(255))
    incorporation_date = Column(String(255))
    approval_date = Column(String(255))
    area  = Column(String(255))
    phone = Column(String(255))
    email = Column(String(255))
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
    company_range = Column(Text)
    create_time = Column(Integer)
    update_time = Column(Integer)

    def __init__(self):
        self.id = 0
        self.logo = ""
        self.name = ""
        self.registration_status = ""
        self.corporate_representative = ""
        self.registered_capital = ""
        self.incorporation_date = ""
        self.approval_date = ""
        self.area  = ""
        self.phone = ""
        self.email = ""
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
        self.company_range = ""
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

    @classmethod
    def query_all(cls):
        session = DBSession()
        o = session.query(Company).all()
        session.close()
        return o
    @classmethod
    def update(cls, company):
        session = DBSession()
        xm_company = session.query(Company).filter(Company.id == company.id).first()
        xm_company.logo = company.logo
        xm_company.name = company.name
        xm_company.name_md5 = company.name_md5
        xm_company.registration_status = company.registration_status
        xm_company.corporate_representative = company.corporate_representative
        xm_company.registered_capital=company.registered_capital
        xm_company.incorporation_date=company.incorporation_date
        xm_company.approval_date=company.approval_date
        xm_company.area=company.area
        xm_company.phone=company.phone
        xm_company.email=company.email
        xm_company.credit_code=company.credit_code
        xm_company.taxpayer_num=company.taxpayer_num
        xm_company.registration_num=company.registration_num
        xm_company.organization_code=company.organization_code
        xm_company.insured_persons=company.insured_persons
        xm_company.enterprise_type=company.enterprise_type
        xm_company.industry=company.industry
        xm_company.old_name=company.old_name
        xm_company.en_name=company.en_name
        xm_company.web=company.web
        xm_company.address=company.address
        xm_company.company_range=company.company_range
        xm_company.update_time=int(time.time())
        session.commit()
        session.close()
    @classmethod
    def get_by_md5(cls, name_md5):
        session = DBSession()
        ret = session.query(Company).filter_by(name_md5=name_md5).first()
        session.close()
        return ret
    @classmethod
    def get_by_id(cls, id):
        session = DBSession()
        ret = session.query(Company).filter_by(id=id).first()
        session.close()
        return ret
