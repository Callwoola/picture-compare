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
        (r"/search_test", demo.TestHandler),

        # ---------------------------------------------
        # static url
        # ---------------------------------------------
        # (r'/img/(.*)', tornado.web.StaticFileHandler, {'path': os.environ[config.STATIC_DIR]}),
        # (r'/tests/(.*)', tornado.web.StaticFileHandler, {'path': os.environ[config.PROJECT_DIR]+"/tests/"}),

        # ---------------------------------------------
        # index
        # ---------------------------------------------
        (r'/_index(.*)',bindex.BuildIndexHandler),
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
