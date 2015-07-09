#coding:utf-8
import tornado
import tornado.ioloop
import tornado.web
import tornado.template
from src.lib import Image
from src.lib import Compare

PROJECT_DIR = "D:/code/image/"
STATIC_DIR = "img/"
PROJECT_DIR_IMG = PROJECT_DIR + "img/"

COMPARE_IMG = "1.jpg"


class SearchHandler(tornado.web.RequestHandler):
    """
    RESTFUL api style
    """
    def get(self):

        # first to decide the picture type by histogram

        # is data is  Smooth  that is material else

        self.write('{error:404}')