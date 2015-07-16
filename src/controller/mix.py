# coding:utf-8
import tornado
import tornado.ioloop
import tornado.web
import tornado.template
from PIL import Image
from src.module import json_module
from src import config
import os
import StringIO
import hashlib
import time


class MixHandler(tornado.web.RequestHandler):
    """
    RESTFUL api style
    """

    def post(self, type=None):
        # -------------------------------------
        # first to get Image file and save
        # response json

        self.set_header('Content-Type', 'application/json')
        jsonM = json_module.json_module()

        imgfiles = self.request.files['file_img']
        if len(imgfiles) > 1:
            return tornado.web.RequestHandler.write(jsonM
                .setStatus('status', 'error')
                .set('msg', 'file error')
                .get())
        print imgfiles
        imgfile = imgfiles[0]
        filename = imgfile['filename'].strip()
        filenname, ext = filename.split('.')

        m = hashlib.md5()
        m.update(str(time.time()) + filename)
        hash = m.hexdigest()
        filename = hash + '.' + ext
        tmp = os.environ[config.PROJECT_DIR] + "img/tmp/"
        tmp_image = tmp + filename
        # -------------------------------
        # all file storage in img/tmp/
        # save filename as tmpfile
        Image.open(StringIO.StringIO(imgfile['body'])).save(tmp_image)
        image_url = os.environ[config.SERVER_URL] + '/img/tmp/' + filename
        type = self.get_argument("type")
        # if type in ("doc", "image","data"):
        # return self.write(jsonM.setStatus('status', 'OK')
        #                       .set('url', str(image_url))
        #                       .set('hash', hash)
        #                       .get())

        json = self.write(jsonM.setStatus('status', 'OK')
            .set('url', str(image_url))
            .set('hash', hash)
            .get())

        self.set_header('Content-Type', 'application/json')  # headers = self.request.headers
        type = self.get_argument("type")
        if type in ("json", "path", "url", "data"):
            if type == 'json':
                # getJson = self.request.body
                getJson = json
                jsonM = json_module.json_module()
                try:
                    import urllib2

                    jsondata = json.loads(getJson)
                    ret = urllib2.urlopen(jsondata['query']['url']).read()
                    m = hashlib.md5()
                    m.update(str(time.time()))
                    section_list = jsondata['query']['url'].split('.')
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
