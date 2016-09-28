# coding:utf-8
import os
import tornado
import tornado.ioloop
import tornado.web
import tornado.template
from src.core.app import App
from src.lib.data import Data

class HomeHandler(App):
    # @tornado.web.asynchronous
    def get(self, param):
        self.set_header('Content-Type', 'application/json')
        the_list = self.manage.search([])
        result = self.data \
                 .set('status', 'ok') \
                 .set('count_data', str(len(the_list))) \
                 .set('config', self.config) \
                 .get()
        self.write(
            result
        )
