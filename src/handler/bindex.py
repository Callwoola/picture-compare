# coding:utf-8
import hashlib
import json, time, os, uuid
import tornado
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.template
from src.lib.data import Data

# from tornado import queues
from tornado import gen

from tinydb import TinyDB, where
from src.service.manage import Manage

class BuildIndexHandler(tornado.web.RequestHandler):
    """
    RESTFUL api style
    """
    def get(self, type=None):
        self.write("please use post method")

    @tornado.gen.coroutine
    def post(self, type=None):
        self.set_header('Content-Type', 'application/json')
        jsonM = Data()

        getJson = self.request.body
        jsondata = json.loads(getJson)

        __url = jsondata['query']['url']
        __name = jsondata['query']['name']
        __id = jsondata['query']['id']
        __data = jsondata['query']['data']
        # 需要参与搜索的字段
        __search = jsondata['query']['search']

        __data['id'] = __id
        # 直接使用  application 的 redis 初始化
        Manage(
            self.application.r
        ).index_image(
            __id,
            __search,
            __data,
            __url,
            __name
        )
        return self.write(jsonM.setStatus('status', 'OK')
                          .set('msg', str('index success!'))
                          .get())

from src.core.app import App

class AddHandler(App):
    def get(self):
        return self.write('[]')

class CleaerIndexHandler(tornado.web.RequestHandler):
    def delete(self, type=None):
        try:
            # os.remove(os.environ[config.STORAGE_INDEX_DB])
            Manage().clear_db()
        except:
            pass
        self.set_header('Content-Type', 'application/json')
        jsonM = Data()
        self.write(jsonM.setStatus('status', 'OK')
                              .set('msg', str('delete index Success!'))
                              .get())
    def get(self, type=None):
        self.write("error method")
