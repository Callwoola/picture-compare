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


class UploadHandler(tornado.web.RequestHandler):
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
        print "has post"
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Content-Type', 'application/json')
        jsonM = json_module.json_module()
        # print self.request.files['file']

        if "file_img" in self.request.files.keys():
            imgfiles = self.request.files['file_img']
        elif "file" in self.request.files.keys():
            imgfiles = self.request.files['file']
        else:
            return self.write(jsonM
                              .setStatus('status', 'error')
                              .set('msg', 'not upload file error')
                              .get())
        # print imgfiles
        # print len(imgfiles)
        if len(imgfiles) > 1:
            return self.write(jsonM
                              .setStatus('status', 'error')
                              .set('msg', 'file error allow one file')
                              .get())
        print "almost right"
        # print imgfiles
        imgfile = imgfiles[0]
        filename = imgfile['filename'].strip()
        filenname, ext = filename.split('.')

        m = hashlib.md5()
        m.update(str(time.time()) + filename)
        hash = m.hexdigest()
        filename = hash + '.' + ext
        tmp = os.environ[config.PROJECT_DIR] + "img/tmp/"
        tmp_image = tmp + filename
        # print tmp_image
        # -------------------------------
        # all file storage in img/tmp/
        # save filename as tmpfile
        Image.open(StringIO.StringIO(imgfile['body'])).save(tmp_image)
        image_url = os.environ[config.SERVER_URL] + '/img/tmp/' + filename
        type = self.get_argument("type")
        if type in ("doc", "image", "data"):
            return self.write(jsonM.setStatus('status', 'OK')
                              .set('url', str(image_url))
                              .set('hash', hash)
                              .get())
