
def get_list():
    list_ = []
    from api.detail_api.api_kanzhunwang_detail import KanzhunwangDetail
    list_.append(['kanzhunwang',KanzhunwangDetail])
    from api.detail_api.api_qichacha_detail import QichachaDetail
    list_.append(['qichacha',QichachaDetail])
    return list_
