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
        self.write(jsonM.set('status', 'error').set('msg','post json').get())

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
                    section_list=jsondata['query']['url'].split('.')
                    tmp_name = os.environ[config.PROJECT_DIR] + 'img/tmp/' + m.hexdigest() + section_list[-1]
                    output = open(tmp_name, 'wb')
                    output.write(ret)
                    output.close()

                    # if ret.code == 200:
                    ''' there is processing img and return img list '''
                    from src.service.compare import Compare
                    compareDict = Compare().setCompareImage(tmp_name)

                    # print compareDict
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
            if type in ("path", "url", "data"):
                ''' get post image file '''
                tornado.web.RequestHandler.write(jsonM
                                                 .set('status', 'error')
                                                 .set('msg', 'waiting')
                                                 .get())
                pass
