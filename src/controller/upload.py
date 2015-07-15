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

    def post(self,type=None):
        # first to get Image file and save
        # response json

        # type = self.get_argument("type")
        self.set_header('Content-Type', 'application/json')
        jsonM = json_module.json_module()
        # from src.lib import Image as ImageTool
        # imagetool=ImageTool.Image()
        # compare = Compare.Image()

        imgfiles = self.request.files['file_img']
        if len(imgfiles) > 1:
            return tornado.web.RequestHandler.write(jsonM
                                             .setStatus('status', 'error')
                                             .set('msg', 'file error')
                                             .get())
        imgfile = imgfiles[0]
        filename = imgfile['filename'].strip()
        filenname,ext=filename.split('.')

        m=hashlib.md5()
        m.update(str(time.time())+filename)
        hash=m.hexdigest()
        filename=hash+'.'+ext
        tmp = os.environ[config.PROJECT_DIR] + "img/tmp/"
        tmp_image = tmp + filename
        # -------------------------------
        # all file storage in img/tmp/
        ''' save filename as tmpfile '''
        Image.open(StringIO.StringIO(imgfile['body'])).save(tmp_image)
        image_url=os.environ[config.SERVER_URL]+'/img/tmp/'+filename
        type = self.get_argument("type")
        if type in ("doc", "image"):
            return self.write(jsonM.setStatus('status', 'OK')
                              .set('url', image_url)
                              .set('hash', hash)
                              .get())

