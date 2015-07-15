# coding:utf-8
import tornado
import tornado.ioloop
import tornado.web
import tornado.template
from src.lib import Image
from src.lib import Compare
from src.module import json_module


class uploadHandler(tornado.web.RequestHandler):
    """
    RESTFUL api style
    """

    def post(self):
        # first to get Image file and save
        # response json

        self.set_header('Content-Type', 'application/json')
        type = self.get_argument("type")
        if type in ("json", "path", "url", "data"):
            hash = ""
            jsonM = json_module.json_module()
            tornado.web.RequestHandler.write(jsonM
                                             .setStatus('status', 'OK')
                                             .set('hash', hash)
                                             .get())
