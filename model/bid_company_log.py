import json
from sqlalchemy import Column
from sqlalchemy.types import *  # 所有字段类型
from . import DBSession
from . import Base


class CompanyLog(Base):
    __tablename__ = "bid_company_log"  # 数据表的名字
    id = Column(Integer, primary_key=True)
    words = Column(String(255))
    msg = Column(String(255))
    ip = Column(String(255))
    code = Column(Integer)
    data = Column(Text)
    create_time = Column(Integer)
    request_time  = Column(Integer)
    api_name = Column(String(255))
    type = Column(String(255))
    error = Column(Text)
    
    def __init__(self):
        self.id = 0
        self.words = ''
        self.msg = ''
        self.ip = ''
        self.code = 0
        self.data = ''
        self.create_time = 0
        self.request_time  = 0
        self.api_name = ''
        self.type = ''
class CompanyLogDao(object):
    def __init__(self):
        self.db = DBSession()

    def __del__(self):
        self.db.close()

    def add(self, company_log):
        sesion = DBSession()
        sesion.add(company_log)
        sesion.commit()
        sesion.close()
    @classmethod
    def query_all(cls):
        session = DBSession()
        o = session.query(CompanyLog).all()
        session.close()
        return o
    def bejson(self,companylog):
        return{
            "id":companylog.id,
            "type":companylog.type,
            "error":companylog.error
        }
    @classmethod
    def get_by_id(cls, id):
        session = DBSession()
        ret = session.query(CompanyLog).filter_by(id=id).first()
        session.close()
        return ret
    @classmethod
    def get_by_words(cls, words):
        session = DBSession()
        ret = session.query(CompanyLog).filter_by(words=words).all()
        session.close()
        return ret
    @classmethod
    def get_by_time(cls, start,end):
        session = DBSession()
        ret = session.query(CompanyLog).filter(CompanyLog.create_time>start,CompanyLog.create_time<end).all()
        session.close()
        return ret
    @classmethod
    def st_error(cls,start,end):
        session = DBSession()
        ret = session.query(CompanyLog).filter(CompanyLog.create_time>start,CompanyLog.create_time<end,CompanyLog.error!='').all()
        session.close()
        return ret
    @classmethod
    def st_words(cls,start,end):
        session = DBSession()
        ret = session.query(CompanyLog).filter(CompanyLog.create_time>start,CompanyLog.create_time<end,CompanyLog.type=='detail').all()
        session.close()
        return ret