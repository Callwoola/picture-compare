# coding:utf-8
import tornado
import tornado.ioloop
import tornado.web
import tornado.template
import json
import StringIO
from src.module import json_module
from src import config
from src.adapter import db
import hashlib, time, os


class pcHandler(tornado.web.RequestHandler):
    """
    picture compare
    RESTFUL api style
    """

    def get(self, type):
        # db.pcDB
        self.set_header('Content-Type', 'application/json')
        jsonM = json_module.json_module()
        jsonM.set('data', [
            # {'material': {
            #     'id': 12
            # }},
            # {'material': "123123"},
            # {'material': "123123"}
        ])
        jsonM.set('status', 'OK')
        if self.get_argument("type") in ("json", "path", "url"):
            def getAll():
                return []

            self.write(jsonM.get())
            return
        self.write(jsonM.set('status', 'error').get())

    def post(self, type):
        '''
        :param type:
        :return:
        '''

        self.set_header('Content-Type', 'application/json')
        # headers = self.request.headers
        type = self.get_argument("type")
        if type in ("json", "path", "url", "data"):
            if type == 'json':
                getJson = self.request.body
                jsonM = json_module.json_module()
                try:
                    import urllib2

                    jsondata = json.loads(getJson)
                    ret = urllib2.urlopen(jsondata['query']['url']).read()
                    m = hashlib.md5()
                    m.update(str(time.time()))
                    tmp_name = os.environ[config.PROJECT_DIR] + 'img/tmp/' + m.hexdigest() + '.png'
                    output = open(tmp_name, 'wb')
                    output.write(ret)
                    output.close()

                    # if ret.code == 200:
                    ''' there is processing img and return img list '''
                    from src.service.compare import Compare

                    compareDict = Compare().setCompareImage(tmp_name)

                    # ret.save('./the.jpg')
                    self.write(jsonM
                               .set('status', 'OK')
                               .set('data', compareDict)
                               .get())
                except Exception, e:
                    print e
                    tornado.web.RequestHandler.write(jsonM
                                                     .set('status', 'error')
                                                     .set('msg', 'json format error!')
                                                     .get())
            if type == 'data':
                pass


class IndexHandler(tornado.web.RequestHandler):
    """
    RESTFUL api style
    """

    def post(self):
        self.set_header('Content-Type', 'application/json')
        post_str = ""
        postJson = json.load(post_str)
        # db.index(post_str)
        pass

    def get(self, *args, **kwargs):
        self.set_header('Content-Type', 'application/json')
        self.write('{error:404}')
        pass
