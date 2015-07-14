# coding:utf-8
import tornado
import tornado.ioloop
import tornado.web
import tornado.template
import json
from src.module import json_module
from src.adapter import db


class pcHandler(tornado.web.RequestHandler):
    """
    picture compare
    RESTFUL api style
    """
    def get(self, type):
        # db.pcDB
        self.set_header('Content-Type', 'application/json')
        jsonM = json_module.json_module()
        jsonM.set('data', [
            {'material': {
                'id': 12
            }},
            {'material': "123123"},
            {'material': "123123"}
        ])
        jsonM.set('status', 'OK')
        if self.get_argument("type") in ("json", "path", "url"):
            def getAll():
                return []

            self.write(jsonM.get())
            return
        self.write(jsonM.set('status', 'error').get())

    def post(self, type):
        self.set_header('Content-Type', 'application/json')
        jsonM = json_module.json_module()

        self.write(jsonM
                   .set('status', 'no')
                   .set('data', 'no')
                   .get())
        pass



class IndexHandler(tornado.web.RequestHandler):
    """
    RESTFUL api style
    """

    def post(self):
        self.set_header('Content-Type', 'application/json')
        post_str = ""
        postJson = json.load(post_str)
        # db.index(post_str)
        pass

    def get(self, *args, **kwargs):
        self.set_header('Content-Type', 'application/json')
        self.write('{error:404}')
        pass
