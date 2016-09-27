# coding:utf-8
import json
import StringIO
import urllib2
import hashlib, time, os
import tornado
import tornado.ioloop
import tornado.web
import tornado.template
from src import config
from src.core.app import App
from src.service.match import Match # 对比管理程序


class pcHandler(App):
    def post(self, type):
        self.set_header('Content-Type', 'application/json')
        # way = self.get_argument("type")

        # if way != 'json':
        #     raise Exception('method incorrect!')

        getJson = self.request.body
        jsondata = json.loads(getJson)

        # 储存对比图片到 redis 
        self.manage.store_base_image(jsondata['query']['url'])

        try:
            terms = jsondata['terms']
        except:
            terms = None
        # 开始比对
        resultDict = Match(
            self.manage
        ).get_match_result(terms)

        self.result(resultDict)
