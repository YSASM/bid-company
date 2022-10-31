import hashlib
import hmac
import os
import urllib.parse

import execjs

base_path = os.path.dirname(__file__)
def key_quote(args):
    """
    关键词转换
    :return:
    """
    result = urllib.parse.quote(args)
    return result.lower()


def get_sign(args):
    """
    获取加密字符串
    :param args:
    :return:
    """
    f = open(os.path.join(base_path,"key.js"), 'r', encoding='utf-8').read()
    context = execjs.compile(f)
    result = context.call('get_en', args)
    return result


# 生成签名
def sign_with_hmac(key, s):
    return hmac.new(bytes(key, encoding='utf-8'), bytes(s, encoding='utf-8'), hashlib.sha512).hexdigest()


def get_key(search_key):
    search_key = key_quote(search_key)
    # 参数
    a = [
        f"/api/search/searchmind?mindkeywords=true&mindtype=9&pagesize=5&person=true&searchkey={search_key}&suggest=true"]
    # 获取加密参数
    en = get_sign(a)
    sign = sign_with_hmac(en, a[0] + "{}")
    return sign[8:28]


def get_value(search_key,tid):
    search_key = key_quote(search_key)
    # 参数
    a = [
        f"/api/search/searchmind?mindkeywords=true&mindtype=9&pagesize=5&person=true&searchkey={search_key}&suggest=true"]
    # 获取加密参数
    en = get_sign(a)
    add_key = "pathString{}" + tid
    a[0] = a[0]+add_key
    sign = sign_with_hmac(en, a[0])
    return sign


if __name__ == '__main__':
    # 搜索词汇
    search_key = "劳保"
    key = get_key(search_key)
    value = get_value(search_key)
    print(key)
    print(value)