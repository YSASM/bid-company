class DetailData(object):
    def __init__(self):
        self.logo = '-'
        self.name = '-'
        self.keyNo = '-'

    def bejson(self,data):
        return {
            'logo':data.logo,
            'name':data.name,
            'keyNo':data.keyNo,
        }
class Detail(object):
    def __init__(self):
        self.code = 0
        self.data = []
        self.type = ''
        self.ip = ""
        self.msg = ""
        self.error = ""
        self.words = ""

    def bejson(self,data):
        return {
            "code": 0 if data.error=="" else 1,#返回状态码
            "words":data.words,#搜索词
            "data": data.data,
            "type": data.type,#api类型（qichacha。
            "count": len(data.data),#公司数
            "error" : data.error,#发生错误
            "ip": data.ip,#请求IP
            "msg": '操作成功' if data.error=="" else '操作失败'#返回状态信息
        }

class ListData(object):
    def __init__(self):
        self.name = '-'
        self.old_name = '-'
        self.registration_status = '-'
        self.corporate_representative = '-'
        self.registered_capital = '-'
        self.incorporation_date = '-'
        self.approval_date = '-'
        self.area = '-'
        self.phone = '-'
        self.email = '-'
        self.credit_code = '-'
        self.taxpayer_num = '-'
        self.registration_num = '-'
        self.organization_code = '-'
        self.insured_persons = 0
        self.enterprise_type = '-'
        self.industry = '-'
        self.en_name = '-'
        self.web = '-'
        self.address = '-'
        self.company_range = '-'

    def bejson(self,data):
        return {
            'name' :data.name,
            'old_name' : data.old_name,
            'registration_status' : data.registration_status,
            'corporate_representative' : data.corporate_representative,
            'registered_capital' : data.registered_capital,
            'incorporation_date' : data.incorporation_date,
            'approval_date' : data.approval_date,
            'area': data.area,
            'phone' : data.phone,
            'email' : data.email,
            'credit_code' : data.credit_code,
            'taxpayer_num' : data.taxpayer_num,
            'registration_num' : data.registration_num,
            'organization_code' : data.organization_code,
            'insured_persons' : data.insured_persons,
            'enterprise_type' : data.enterprise_type,
            'industry' : data.industry,
            'en_name' : data.en_name,
            'web'  : data.web,
            'address' : data.address,
            'company_range' : data.company_range
        }   
class List(object):
    def __init__(self):
        self.code = 0
        self.data = []
        self.type = ''
        self.ip = ""
        self.msg = ""
        self.error = ""
        self.words = ""

    def bejson(self,data):
        return {
            "code": 0 if data.error=="" else 1,#返回状态码
            "words":data.words,#搜索词
            "data": data.data,
            "type": data.type,#api类型
            "error" : data.error,#发生错误
            "ip": data.ip,#请求ip
            "msg": '操作成功' if data.error=="" else '操作失败'#返回状态信息
        }
class Log(object):
    def __init__(self):
        self.code = 0
        self.logs = []
        self.msg = ""
        self.error = ""

    def bejson(self,data):
        return {
            "code": 0 if data.error=="" else 1,
            "data": data.logs,
            "count":len(data.logs),
            "error" : data.error,#发生错误
            "msg": '操作成功' if data.error=="" else '操作失败'#返回状态信息
        }