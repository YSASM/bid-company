def get_list():
    list_ = []
    from api.list_api.api_qichacha_list import Qichacha_list
    list_.append(Qichacha_list)
    return list_