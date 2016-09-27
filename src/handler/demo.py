# coding:utf-8
import os
import glob
import StringIO
import tornado
import tornado.ioloop
import tornado.web
import tornado.template
from PIL import Image as im

from src import config
from src.core.app import App
from src.lib.image import Image
from src.service.feature import Feature as Compare
from src.service.manage import Manage as Manage
from src.service.match import Match



class TestHandler(App):
    def get(self, *args, **kwargs):
        self.write(
            tornado.template.Loader(os.environ[config.TEMPLATE]).load("search_test_upload.html").generate(
                name='search by index',
                action='search_test'
            )
        )

    def post(self, *args, **kwargs):
        '''
        search color test demo
        '''
        os.chdir(os.environ[config.PROJECT_DIR] + "tests/tmp/")
 
        imagetool = im
        compare = Compare()
        imgfiles = self.request.files['file_img']
        if len(imgfiles) > 1:
            return self.write("error")
        imgfile = imgfiles[0]
        filename = imgfile['filename'].strip()
        import uuid
        filename = str(uuid.uuid4()) + '.' + filename.split('.')[-1]
        tmp = os.environ[config.PROJECT_DIR] + "tests/tmp/"

        tmp_image = tmp + filename
        print tmp_image
        im.open(StringIO.StringIO(imgfile['body'])).save(tmp_image)

        # path = os.environ[config.PROJECT_DIR] + "tests/img/"
        self.m.store_base_image_file(tmp_image)


        # 开始比对
        resultDict = Match(
            self.m
        ).get_match_result()
        
        print resultDict
        self.write(
            tornado.template.Loader(os.environ[config.TEMPLATE]).load("search_test.html").generate(
                origin_img = '/tests/tmp/' + filename,
                results = resultDict
            )
        )
