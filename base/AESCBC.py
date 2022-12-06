import json
import execjs


def get_detail_encrypt_data(input, iv):
    """
    获取详情加密数据
    :return:
    """
    f = open('base/js/kanzhunwang.js', 'r', encoding='utf-8')
    context = execjs.compile(f.read())
    f.close()
    result = context.call('encrypt', json.dumps(input), iv)
    return result


def get_encrypt_data(key_id, iv):
    """
    获取加密数据
    :return:
    """
    f = open('base/js/kanzhunwang.js', 'r', encoding='utf-8')
    context = execjs.compile(f.read())
    f.close()
    result = context.call('encrypt', json.dumps({"encCompanyId": key_id}), iv)
    return result


def get_decrypt_data(data, iv):
    """
    获取解密数据
    :return:
    """
    f = open('base/js/kanzhunwang.js', 'r', encoding='utf-8')
    context = execjs.compile(f.read())
    f.close()
    result = context.call('decrypt', data, iv)
    return result
