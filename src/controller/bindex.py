# coding:utf-8
import tornado
import tornado.ioloop
import tornado.web
import tornado.template

from src.module import json_module


class BuildIndexHandler(tornado.web.RequestHandler):
    """
    RESTFUL api style
    """

    def post(self, type=None):
        # -------------------------------------
        # first to get Image file and save
        # response json

        self.set_header('Content-Type', 'application/json')
        jsonM = json_module.json_module()
        return tornado.web.RequestHandler.write(jsonM
                                                .setStatus('status', 'error')
                                                .set('msg', 'file error')
                                                .get())
