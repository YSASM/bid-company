import json
import hashlib
import time
from sqlalchemy import Column
from sqlalchemy.types import *  # 所有字段类型
from . import DBSession
from . import Base


class Admin(Base):
    __tablename__ = "bid_admin"  # 数据表的名字
    id = Column(Integer, primary_key=True)
    username = Column(String(20))
    nickname = Column(String(50))
    realname = Column(String(64))
    password = Column(String(32))
    salt = Column(String(30))
    avatar = Column(String(255))
    email  = Column(String(100))
    loginip = Column(String(5))
    status = Column(String(30))
    mobile = Column(String(32))
    prev_time = Column(Integer)
    token = Column(String(59))
    expire_time = Column(Integer)
    login_time = Column(Integer)
    create_time = Column(Integer)
    update_time = Column(Integer)
    def __init__(self):
        self.id = 0
        self.username = ''
        self.nickname = ''
        self.realname = ''
        self.password = ''
        self.salt = ''
        self.avatar = ''
        self.email  = ''
        self.loginip = ''
        self.status = ''
        self.mobile = ''
        self.prev_time = 0
        self.token = ''
        self.expire_time = 0
        self.login_time = 0
        self.create_time = 0
        self.update_time = 0
class AdminDao(object):
    def __init__(self):
        self.db = DBSession()

    def __del__(self):
        self.db.close()
    @classmethod
    def update(cls, admin):
        session = DBSession()
        xm_admin = session.query(Admin).filter(Admin.username == admin.username,Admin.password == admin.password).first()
        xm_admin.loginip = admin.loginip
        xm_admin.login_time=int(time.time())
        session.commit()
        session.close()
    @classmethod
    def query_all(cls):
        session = DBSession()
        o = session.query(Admin).all()
        session.close()
        return o
    @classmethod
    def login(cls,username,password):
        session = DBSession()
        o = session.query(Admin).filter(Admin.username == username).all()
        session.close()
        password = hashlib.md5(password.encode("utf-8")).hexdigest()
        if not o:
            return False
        for i in o:
            if i.password == hashlib.md5((password+i.salt).encode("utf-8")).hexdigest():
                return True
            return False
        return False