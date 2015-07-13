#coding:utf-8
import tornado
import tornado.ioloop
import tornado.web
import tornado.template
from src.lib import Image
from src.lib import Compare



class SearchHandler(tornado.web.RequestHandler):
    """
    RESTFUL api style
    """
    def get(self):

        # first to decide the picture type by histogram

        # is data is  Smooth  that is material else

        self.write('{error:404}')


class JsonHandler(tornado.web.RequestHandler):
    """
    RESTFUL api style
    """
    def get(self):

        # first to decide the picture type by histogram

        # is data is  Smooth  that is material else

        self.write('{error:404}')