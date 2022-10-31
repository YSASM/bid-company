from service.company import CompanyService
from model.bid_company import CompanyDao
from config.config import Config
import logging
from base.http_wrapper import HttpWrapper

SpiderAjaxHeader = {
    "Content-Type": "application/json",
    "Connection": "close",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36",
}

SpiderHtmlHeader = {
    "Content-Type": "text/html",
    "Connection": "close",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36",
}

GET = 'get'
POST = 'post'
OPTIONS = 'options'
HEAD = 'head'
PUT = 'put'
PATCH = 'patch'
DELETE = 'delete'
TargetType = {
    '.doc': 'word',
    '.docx': 'word',
    '.pdf': 'pdf',
    '.ppt': 'ppt',
    '.xls': 'excel',
    '.xlsx': 'excel',
    '.txt': 'text',
    '.jpg': 'image',
    '.png': 'image',
    '.jpeg': 'image',
}


class ApiBase(object):
    def __init__(self):
        self._company_service = CompanyService()
        self._company_dao = CompanyDao()

    def add(self, info):
        try:
            self._company_dao.add(info)
        except Exception as e:
            logging.error('add company fail %s', str(e))

    def exist(self, company):
        return self._company_dao.exist(company.name)
    
    def http_wrapper(self, method, url, headers=SpiderHtmlHeader, cookies=None, timeout=30, **kwargs):
        if method == GET:
            content = HttpWrapper.get(url=url, headers=headers, cookies=cookies,
                                      timeout=timeout, **kwargs)
        elif method == POST:
            content = HttpWrapper.post(url=url, headers=headers, cookies=cookies,
                                       timeout=timeout, **kwargs)
        back_code, back_content = content
        if back_code == 'pass':
            return None
        elif back_code == 'error':
            logging.warning(f"【{self.source.name}】【{self.source.spider}】【网络超时】 ：url : {url},error:{back_content}")
            return None
        elif back_code == 'bad':
            logging.warning(f"【{self.source.name}】【{self.source.spider}】【网络错误】 ：url : {url},error:{back_content}")
            return None
        elif back_code == 'ok':
            return back_content

    def replace_warpper(self, string: str, list_replace=['\n', '\r', '\t', ' ']):
        for i in list_replace:
            string = string.replace(i, '')
        return string
