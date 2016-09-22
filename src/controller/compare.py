# coding:utf-8
import tornado
import tornado.ioloop
import tornado.web
import tornado.template
import json
import StringIO
from src import config

import hashlib, time, os
from src.lib.manage import Manage
# 对比管理程序
from src.service.match import Match
import urllib2
from src.core.app import App

class pcHandler(App):
    def post(self, type):
        # way = self.get_argument("type")

        # if way != 'json':
        #     raise Exception('method incorrect!')

        getJson = self.request.body
        jsondata = json.loads(getJson)

        # 储存对比图片到 redis 
        Manage().store_base_image(jsondata['query']['url'])
        terms = jsondata['terms']

        # 开始比对
        resultDict = Match().setCompareImage(terms)

        self.result(resultDict)
