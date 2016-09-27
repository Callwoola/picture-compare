# coding:utf-8
import os
import tornado
import tornado.ioloop
import tornado.web
import tornado.template
from src import config
from src.lib.data import Data

class HomeHandler(tornado.web.RequestHandler):
    # @tornado.web.asynchronous
    def get(self, param):
        self.set_header('Content-Type', 'application/json')
        jsonM = Data()
        result = jsonM \
                 .set('status', 'ok') \
                 .set('demo_url', '/demo') \
                 .set('count_data', '0') \
                 .get()
        self.write(
            result
        )
