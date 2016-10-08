# coding:utf-8
import json
from src.core.app import App

class pcHandler(App):
    def post(self, type):
        self.set_header('Content-Type', 'application/json')
        # way = self.get_argument("type")

        # if way != 'json':
        #     raise Exception('method incorrect!')

        getJson = self.request.body
        jsondata = json.loads(getJson)

        # 储存对比图片到 redis
        if 'base64' in jsondata['query'].keys():
            self.manage.store_base_image_by_base64(jsondata['query']['base64'])
        else:
            self.manage.store_base_image(jsondata['query']['url'])

        try:
            terms = jsondata['terms']
        except:
            terms = None

        # 返回数据限定
        try:
            page_size = jsondata['size']
        except:
            page_size = None

        # 开始比对
        resultDict = self.match.get_match_result(terms, page_size)

        self.result(resultDict)
