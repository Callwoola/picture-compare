# coding:utf-8
import tornado
import tornado.ioloop
import tornado.web
import tornado.template
from src.handler import (demo,compare,bindex,home)
import os

def getRoutes(config):
    Routes = [


        # ---------------------------------------------
        # demo url
        # ---------------------------------------------
        (r"/demo", demo.DemoHandler),
        (r"/search", demo.DemoSearchHandler),
        (r"/search_color", demo.DemoSearchColorHandler),
        (r"/upload_search", demo.DemoUploadSearchHandler),
        (r"/upload_search_color", demo.DemoUploadSearchColorHandler),

        # ---------------------------------------------
        # static url
        # ---------------------------------------------
        (r'/img/(.*)', tornado.web.StaticFileHandler, {'path': os.environ[config.STATIC_DIR]}),
        (r'/tests/(.*)', tornado.web.StaticFileHandler, {'path': os.environ[config.PROJECT_DIR]+"/tests/"}),

        # ---------------------------------------------
        # index
        # ---------------------------------------------
        # (r'/_search/json/(.*)', search.JsonHandler),
        # (r'/_upload(.*)',upload.UploadHandler),
        # (r'/_mix(.*)',mix.MixHandler),
        # (r'/_color(.*)',compare.pcHandler),
        (r'/_index(.*)',bindex.BuildIndexHandler),
        (r'/_add(.*)', bindex.AddHandler),
        (r'/_delete(.*)', bindex.CleaerIndexHandler),


        # picture compare api
        (r'/_pc(.*)',compare.pcHandler),

        # ---------------------------------------------
        # other tool url
        # ---------------------------------------------
        # (r'/crossdomain.xml',urltool.urltoolHandler),
        
        # ---------------------------------------------
        # home dashboard url
        # ---------------------------------------------
        (r"/(.*)", home.HomeHandler),
    ]

    return Routes
