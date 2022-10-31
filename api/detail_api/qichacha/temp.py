import requests
import re
headers = {
    'authority': 'www.qcc.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': 'QCCSESSID=440534533477b8c66e2742e64b; qcc_did=2d9ccd44-622d-476c-afa0-fab8d2251d91; UM_distinctid=18426c98c7228f-087762e052679e-26021f51-1fa400-18426c98c73fec; acw_tc=78d1899916671091583886990eb2efaa074d9863ef4320e28c096c5eea; CNZZDATA1254842228=1065001700-1667095186-https%253A%252F%252Fwww.baidu.com%252F%7C1667109245',
    'referer': 'https://www.qcc.com/web/search?key=%E4%B8%87%E8%BE%BE%E9%9B%86%E5%9B%A2',
    'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}

params = (
    ('key', '\u4E07\u8FBE\u96C6\u56E2'),
)

response = requests.get('https://www.qcc.com/web/search', headers=headers, params=params,verify=False)
result = re.search("window.tid='(.{32})'<",response.text,re.S).group(1)
print(result)
#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://www.qcc.com/web/search?key=%E4%B8%87%E8%BE%BE%E9%9B%86%E5%9B%A2', headers=headers)
