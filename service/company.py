import re
from model.bid_company import CompanyDao


class CompanyService(object):
    # name = {}
    name_md5 = {}
    # id = {}
    # logo = {}
    def __init__(self):
        self.companys = CompanyDao.query_all()
        for company in self.companys:
        #     self.id[int(company.id)] = company
        #     self.name[str(company.name)] = company
            self.name_md5[str(company.name_md5)] = company
        #     self.logo[str(company.logo)] = company
    def exist(self, md5):
        self.companys = CompanyDao.query_all()
        for company in self.companys:
        #     self.id[int(company.id)] = company
        #     self.name[str(company.name)] = company
            self.name_md5[str(company.name_md5)] = company
        if md5 in self.name_md5:
            return True
        return False
    def match_companys(self,md5):
        for company in self.companys:
            if company.name_md5 == md5:
                return company
        return None
        
    def match_detail_companys(self,key):
        """
        模糊查找器
        :param key: 关键字
        :param data: 数据
        :return: list
        """
        # 结果列表
        suggestions = []
        # 非贪婪匹配，转换 'djm' 为 'd.*?j.*?m'
        # pattern = '.*?'.join(key)
        pattern = '.*%s.*'%(key)
        # print("pattern",pattern)
        # 编译正则表达式
        regex = re.compile(pattern)
        for item in self.companys:
            # print("item",item['name'])
            # 检查当前项是否与regex匹配。
            match = regex.search(item.name)
            if match:
                # 如果匹配，就添加到列表中
                suggestions.append([item.id,item.name,item.logo,item.corporate_representative,item.registered_capita ,item.incorporation_date ])
        return suggestions