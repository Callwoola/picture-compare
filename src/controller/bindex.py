# coding:utf-8
import tornado
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.template
import json, time, os, uuid
from src.service.data import Data
import hashlib
from src import config

# from tornado import queues
from tornado import gen

from tinydb import TinyDB, where
from src.lib.Manage import Manage

class BuildIndexHandler(tornado.web.RequestHandler):
    """
    RESTFUL api style
    """
    def get(self, type=None):
        self.write("please use post method")
        
    @tornado.gen.coroutine
    def post(self, type=None):
        # rebuild db
        # db = TinyDB(os.environ[config.STORAGE_INDEX_DB])

        # -------------------------------------
        # first to get Image file and save
        # response json
        # type = self.get_argument("type")

        # type in ( insert update delete )
        self.set_header('Content-Type', 'application/json')
        # jsonM = json_module.json_module()
        jsonM = Data()

        # tornado.ioloop.IOLoop().run_sync(the_queue)
        getJson = self.request.body

        jsondata = json.loads(getJson)
        # print jsondata
        __url = jsondata['query']['url']
        __name = jsondata['query']['name']
        __id = jsondata['query']['id']
        __data = jsondata['query']['data']
        # 需要参与搜索的字段
        __search = jsondata['query']['data']
        
        # keys = {}
        # # 针对 dmc 分类的预定义
        # keys["l"] = __data['leaf_category']
        # keys["r"] = __data['root_category']

        Manage().index_image(
            __id,
            __search,
            keys,
            __data,
            __url
        )
        return self.write(jsonM.setStatus('status', 'OK')
                          .set('msg', str('index success!'))
                          .get())

        # import urllib2
        # print json
        # ret = urllib2.urlopen(jsondata['query']['url'])
        # if ret.code == 200:
        #     # ------------------------
        #     # storage file
        #     m = hashlib.md5()
        #     m.update(str(time.time()))

        #     tmp_name = os.environ[config.PROJECT_DIR] + 'img/storage/' + \
        #                m.hexdigest() + '.' + \
        #                jsondata['query']['url'].split('.')[-1]

        #     output = open(tmp_name, 'wb')
        #     output.write(ret.read())
        #     output.close()
        #     # ----------------------
        #     # build index
        #     id = str(uuid.uuid4())
        #     print __data
        #     db.insert({'id': id,
        #                'data': {
        #                    'id': __id,
        #                    'url': __url,
        #                    'map': tmp_name,
        #                    'name': __name,
        #                    'data': __data
        #                }})
        #     return self.write(jsonM.setStatus('status', 'OK')
        #                       .set('msg', str('index success!'))
        #                       .get())
        # else:
        #     return self.write(jsonM.setStatus('status', 'error')
        #                       .set('msg', str('file error'))
        #                       .get())

from src.core.app import App

class AddHandler(App):
    def get(self):
        return self.write('[]')

class CleaerIndexHandler(tornado.web.RequestHandler):
    def delete(self, type=None):
        try:
            os.remove(os.environ[config.STORAGE_INDEX_DB])
        except:
            pass
        self.set_header('Content-Type', 'application/json')
        jsonM = Data()
        self.write(jsonM.setStatus('status', 'OK')
                              .set('msg', str('delete index Success!'))
                              .get())
    def get(self, type=None):
        self.write("error method")
