# coding:utf-8
import tornado
import tornado.ioloop
import tornado.web
import tornado.template
from src.lib import image
from src.lib import manage
from src.lib import feature
from src import config
import os
from src.lib.manage import Manage
from src.service.data import Data

class HomeHandler(tornado.web.RequestHandler):
    def get(self, param):
        print param
        self.set_header('Content-Type', 'application/json')
        jsonM = Data()
        # the_list = Manage().all()
        result = jsonM \
                 .set('status', 'ok') \
                 .set('demo_url', '/demo') \
                 .set('count_data', '0') \
                 .get()
        self.write(
            result
        )
