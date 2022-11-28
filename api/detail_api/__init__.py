import json
def read_json():
    on_off = open('base/on_off.json','r')
    on_off = json.load(on_off)['data']
    return on_off
def get_list():
    list_=[]
    from api.detail_api.api_kanzhunwang_detail import api_kanzhunwang_detail
    list_.append(['kanzhunwang',api_kanzhunwang_detail,"1"])
    from api.detail_api.api_qichacha_detail import api_qichacha_detail
    list_.append(['qichacha',api_qichacha_detail,"1"])
    from api.detail_api.api_yuanlue_detail import api_yuanlue_detail
    list_.append(['yuanlue',api_yuanlue_detail,"1"])#yuanlue开关
    on_off = read_json()
    for i in list_:
        for j in on_off:
            if i[0]!=j['name']:
                continue
            if j['status']=="2":
                list_[list_.index(i)][2] = "2"
                break
            else:
                list_[list_.index(i)]{2} = "1"
                break
    return list_
