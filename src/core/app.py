# -*- coding: utf-8 -*-
import json, time, os, uuid
import hashlib

from tornado import gen
import tornado
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.template

from src import config
from src.lib.data import Data
from src.service.manage import Manage
from src.service.match import Match # 对比管理程序

class App(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    # def __init__(self, application, request, **kwargs):
    #     super(tornado.web.RequestHandler, self).__init__(*request,**kwargs)
    def __init__(self, *request, **kwargs):
        super(App, self).__init__(request[0], request[1])

        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

        self.data = Data()
        self.config = self.application.config
        self.manage = Manage(
            self.application.r
        )

        # 定义 匹配接口
        self.match = Match(
            self.manage
        )

    # 数据结果
    def result(self, resultDict = []):
        # print compareDict
        self.write(self.data
                   .set('status', 'OK')
                   .set('data', resultDict)
                   .get())

    def add_json(self):
        self.set_header('Content-Type', 'application/json')

    """
    picture compare
    RESTFUL api style
    """
    def get(self, type):
        # db.pcDB
        self.set_header('Content-Type', 'application/json')
        jsonM = json_module.json_module()
        self.write(jsonM.set('status', 'error').set('msg','post json').get())
