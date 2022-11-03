def get_list():
    list_ = []
    from api.list_api.api_kanzhunwang_list import KanzhunwangList
    list_.append(['kanzhunwang',KanzhunwangList])
    from api.list_api.api_qichacha_list import QichachaList
    list_.append(['qichacha',QichachaList])
    return list_