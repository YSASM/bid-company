import time
import requests
import execjs
class GetXingtuInfo(object):

    headers = {
        'cookie': 'sessionid_ss=0792d151a61aa76ce8285f90a14ec384;',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }
    f = open(r'static/xingtu.js', 'r', encoding='utf-8').read()
    context = execjs.compile(f)

    def get_sign(self, methods, args):
        result = self.context.call(methods, args)
        return result


    def get_sign1(self, page):
        result = self.context.call("get_sign1", page)
        return result


    def get_sign2(self, challenge_id):
        result = self.context.call("get_sign2", challenge_id)
        return result


    def get_amount(self, challenge_id):
        """
        通过 challenge_id 获取 抖音短视频的花费金额
        :param challenge_id:
        :return: amount
        """
        params = (
            ('challenge_id', challenge_id),
            ('service_name', 'challenge.AdStarChallengeService'),
            ('service_method', 'DemanderGetChallenge'),
            ('sign_strict', '1'),
            ('sign', self.get_sign2(challenge_id)),
        )

        response = requests.get('https://www.xingtu.cn/h/api/gateway/handler_get/', headers=self.headers, params=params)
        data = response.json().get('data')
        price = data.get('progress').get('reward_amount')
        price = int(round(float(int(price) / 1000), 0))
        return price


    def get_order_list(self, page):
        params = (
            ('limit', '10'),
            ('page', f"{page}"),
            ('query', '{"is_prefer":false,"system_type":1}'),
            ('service_name', 'task.AdStarTaskService'),
            ('service_method', 'DemanderGetUniversalDemandList'),
            ('sign_strict', '1'),
            ('sign', self.get_sign1(page)),
        )

        response = requests.get('https://www.xingtu.cn/h/api/gateway/handler_get/', headers=self.headers, params=params)
        data = response.json().get('data')
        order_list = data.get('demand_info_list')
        return order_list


    def run(self):
        page = 1
        while True:
            order_list = self.get_order_list(page)
            if not order_list:
                break
            for order in order_list:
                # 定单信息
                challenge_info = order.get('challenge_info')
                if challenge_info:
                    if order.get('challenge_info').get('status') == 11:
                        continue
                    else:
                        print('抖音短视频')
                        challenge_id = order.get('challenge_info').get('challenge_id')
                        demand_name = order.get("demand_info").get('demand_name')
                        # print(challenge_id, "challenge_id")
                        print(demand_name)
                        print(self.get_amount(challenge_id))
                        print("=========================" * 3)
                else:
                    order_info = order.get('order_info_list')[0].get('order_info')
                    if order_info.get('origin_status') != 0:
                        continue
                    # 定单价格
                    order_price = order.get('total_pay')
                    # 作者名字
                    auther = order.get('order_info_list')[0].get('author_info').get('nick_name')
                    # 定单时间
                    order_time = order.get('order_info_list')[0].get('order_info').get('release_time')
                    order_time = time.strftime("%Y-%m-%d %H:%S", time.localtime(int(order_time)))
                    print('抖音传播')
                    print(auther)
                    print(order_price)
                    print(order_time)
                    print("=========================" * 3)
            page += 1


    def search_key(self, input_key):
        """
        搜索关键词
        :return: 星图id
        """
        params = (
            ('platform_source', '1'),
            ('key', input_key),
            ('order_by', 'score'),
            ('sort_type', '2'),
            ('search_scene', '1'),
            ('display_scene', '1'),
            ('limit', '20'),
            ('page', '1'),
            ('regular_filter', '{"current_tab":3,"marketing_target":1,"task_category":1}'),
            ('attribute_filter', '{}'),
            ('author_pack_filter', '{}'),
            ('author_list_filter', '{}'),
            ('service_name', 'go_search.AdStarGoSearchService'),
            ('service_method', 'SearchForStarAuthors'),
            ('sign_strict', '1'),
            ('sign', self.get_sign("search_key", input_key)),
        )

        response = requests.get('https://www.xingtu.cn/h/api/gateway/handler_get/', headers=self.headers, params=params)
        data = response.json().get('data').get('authors')
        back = []
        for d in data:
            back.append(d.get("star_id"))
        return back


    def get_shoping(self, start_id):
        """
        获取粉丝数量、月覆盖用户数、月深度用户数
        :return:
        """
        params = (
            ('o_author_id', start_id),
            ('platform_source', '1'),
            ('platform_channel', '1'),
            ('range', '2'),
            ('service_name', 'data_space.AdStarDataSpaceService'),
            ('service_method', 'GetAuthorShoppingInfo'),
            ('sign_strict', '1'),
            ('sign', self.get_sign("shoping", start_id)),
        )

        response = requests.get('https://www.xingtu.cn/h/api/gateway/handler_get/', headers=self.headers, params=params)
        data = response.json()
        return data


    def get_prices(self, start_id):
        """
        获取报价服务
        :param start_id:
        :return: json
        """
        params = (
            ('o_author_id', start_id),
            ('platform_source', '1'),
            ('platform_channel', '1'),
            ('service_name', 'author.AdStarAuthorService'),
            ('service_method', 'GetAuthorMarketingInfo'),
            ('sign_strict', '1'),
            ('sign', self.get_sign("authorService", start_id)),
        )

        response = requests.get('https://www.xingtu.cn/h/api/gateway/handler_get/', headers=self.headers, params=params)

        price_data = []
        data = response.json().get("data").get("price_info")
        for i in data:
            price_data.append({"desc": i.get('desc'), "price": i.get("price")})
        return price_data


    def getAuthorLinkScore(self, start_id):
        """
        获取星图指数
        :return:
        """
        params = (
            ('o_author_id', start_id),
            ('platform_source', '1'),
            ('platform_channel', '1'),
            ('industy_tag', '0'),
            ('service_name', 'data_space.AdStarDataSpaceService'),
            ('service_method', 'GetAuthorLinkScore'),
            ('sign_strict', '1'),
            ('sign', self.get_sign("authorLinkSource", start_id)),
        )

        response = requests.get('https://www.xingtu.cn/h/api/gateway/handler_get/', headers=self.headers, params=params)

        return response.json()


    def getAuthorSpreadInfo(self, start_id):
        """
        获取传播表现数据
        :return:
        """
        params = (
            ('o_author_id', start_id),
            ('platform_source', '1'),
            ('platform_channel', '1'),
            ('range', '2'),
            ('type', '1'),
            ('service_name', 'data_space.AdStarDataSpaceService'),
            ('service_method', 'GetAuthorSpreadInfo'),
            ('sign_strict', '1'),
            ('sign', self.get_sign("getAuthorSpreadInfo",start_id)),
        )

        response = requests.get('https://www.xingtu.cn/h/api/gateway/handler_get/', headers=self.headers, params=params)
        responseData = {}
        data = response.json().get("data")
        responseData["play_over_rate"] = data.get("play_over_rate").get("value")
        responseData["interact_rate"] = data.get("interact_rate").get("value")
        responseData["play_mid"] = data.get("item_rate").get("play_mid").get("value")
        return responseData


    def getAuthorWatchedDistribution(self, start_id):
        """
        受众画像
        :return:
        """
        params = (
            ('o_author_id', start_id),
            ('platform_source', '1'),
            ('platform_channel', '1'),
            ('type', '1'),
            ('service_name', 'data.AdStarDataService'),
            ('service_method', 'GetAuthorWatchedDistribution'),
            ('sign_strict', '1'),
            ('sign', self.get_sign("getAuthorWatchedDistribution",start_id)),
        )

        response = requests.get('https://www.xingtu.cn/h/api/gateway/handler_get/', headers=self.headers, params=params)
        return response.json()
    def get(self,words,xingtu):
        xt = GetXingtuInfo()
        start_ids = xt.search_key(words)
        back = []
        for start_id in start_ids:
            back.append({
                "id" : start_id,
                "shoping" : xt.get_shoping(start_id)['data'],
                "price" : xt.get_prices(start_id),
                "source" : xt.getAuthorLinkScore(start_id)['data'],
                "spreadInfo" : xt.getAuthorSpreadInfo(start_id),
                "authorwatcheddistribution" : xt.getAuthorWatchedDistribution(start_id)['data']
            })
        xingtu.data = back
        return xingtu
    def GetSearch(self,inputKey,xingtu):
        params = (
            ('platform_source', '1'),
            ('key', inputKey),
            ('order_by', 'score'),
            ('sort_type', '2'),
            ('search_scene', '1'),
            ('display_scene', '1'),
            ('limit', '20'),
            ('page', '1'),
            ('regular_filter', '{"current_tab":3,"marketing_target":1,"task_category":1}'),
            ('attribute_filter', '{}'),
            ('author_pack_filter', '{}'),
            ('author_list_filter', '{}'),
            ('service_name', 'go_search.AdStarGoSearchService'),
            ('service_method', 'SearchForStarAuthors'),
            ('sign_strict', '1'),
            ('sign', self.get_sign("SearchForStarAuthors", inputKey)),
        )

        response = requests.get('https://www.xingtu.cn/h/api/gateway/handler_get/', headers=self.headers, params=params)
        data = response.json().get("data").get("authors")
        back = []
        for d in data:
            d = d.get("attribute_datas")
            # follower
            follower = d.get("follower")
            # 预期cpm prospective_20_60_cpm
            cpm = d.get("prospective_20_60_cpm")
            # pro_play expected_play_num
            pro_play = d.get("expected_play_num")
            back.append({
                "name" : inputKey,
                "follower" : follower,
                "cpm" : cpm,
                "pro_play" : pro_play
            })
        
        xingtu.data = back
        return xingtu
if __name__ == '__main__':
    xt = GetXingtuInfo()
    print(xt.GetSearch("工程那些事"))
#     start_id = xt.search_key("酒水那些事")
#     print("星图id: ", start_id)
#     shop_data = xt.get_shoping(start_id)
#     print("粉丝覆盖率：", shop_data)
#     price_data = xt.get_prices(start_id)
#     print("达人服务报价", price_data)
#     source = xt.getAuthorLinkScore(start_id)
#     print("星图指数：", source)
#     spreadInfo = xt.getAuthorSpreadInfo(start_id)
#     print("传播表现：", spreadInfo)
#     getAuthorWatchedDistribution = xt.getAuthorWatchedDistribution(start_id)
#     print("受众画像：", getAuthorWatchedDistribution)
