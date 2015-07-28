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
import json

class MixHandler(tornado.web.RequestHandler):
    """
    RESTFUL api style
    """

    SUPPORTED_METHODS = ("CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")

    def get(self, type=None):
        # print "has post"
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        return self.set_status(204)

    def options(self, type=None):
        # print "has options"
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        return self.set_status(204)

    def post(self, type=None):
        # -------------------------------------
        # first to get Image file and save
        # response json
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Content-Type', 'application/json')
        jsonM = json_module.json_module()

        # imgfiles = self.request.files['file_img']

        if "file_img" in self.request.files.keys():
            imgfiles = self.request.files['file_img']
        elif "file" in self.request.files.keys():
            imgfiles = self.request.files['file']
        else:
            return self.write(jsonM
                              .setStatus('status', 'error')
                              .set('msg', 'not upload file error')
                              .get())

        if len(imgfiles) > 1:
            return tornado.web.RequestHandler.write(jsonM
                .setStatus('status', 'error')
                .set('msg', 'file error')
                .get())
        # print imgfiles
        imgfile = imgfiles[0]
        filename = imgfile['filename'].strip()

        # filenname, ext = filename.split('.')

        file_vals= filename.split('.')
        ext=file_vals[-1]
        filenname=filename.replace(ext,'')

        m = hashlib.md5()
        try:
            # m.update(str(time.time()) + filename)
            m.update(str(time.time()))
        except Exception,e:
            m.update(str(time.time()))
            # m.update(str(time.time()) + filename.decode('gb2312'))
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

        try:
            import urllib2

            ''' there is processing img and return img list '''
            from src.service.compare import Compare

            compareDict = Compare().setCompareImage(tmp_image)

            # print compareDict
            return self.write(jsonM
                .set('status', 'OK')
                .set('data', compareDict)
                .get())
        except Exception, e:
            print e
            return self.write(jsonM
                .set('status', 'error')
                .set('msg', 'json format error!')
                .get())

