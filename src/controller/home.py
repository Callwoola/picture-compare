# coding:utf-8
import tornado
import tornado.ioloop
import tornado.web
import tornado.template
from src.lib import Image
from src.lib import Manage
from src.lib import Compare
from src import config
import os
from src.lib.Manage import Manage
from src.module import json_module

class HomeHandler(tornado.web.RequestHandler):
    def get(self, param):
        print param
        self.set_header('Content-Type', 'application/json')
        jsonM = json_module.json_module()
        the_list = Manage().all()
        result = jsonM.set('status', 'ok') \
                    .set('count_data', str(len(the_list))) \
                    .get()
        self.write(
            result
        )
