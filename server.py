# coding:utf-8
import tornado
import tornado.ioloop
import tornado.web
import tornado.template
from controller import demo

PROJECT_DIR = "D:/code/image/"
STATIC_DIR = "img/"
PROJECT_DIR_IMG = PROJECT_DIR + "img/"


# settings = {'debug': True}
application = tornado.web.Application([
    (r"/", demo.DemoHandler),
    (r"/search", demo.DemoSearchHandler),
    (r"/upload_search", demo.DemoUploadSearchHandler),
    # (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': "D:/code/image/static"}),

    (r'/img/(.*)', tornado.web.StaticFileHandler, {'path': PROJECT_DIR_IMG}),
    (r'/tests/(.*)', tornado.web.StaticFileHandler, {'path': PROJECT_DIR+'/tests/img'}),
])

if __name__ == "__main__":
    application.listen(8888)
    application.debug = True
    # application.autoreload=False
    tornado \
        .ioloop \
        .IOLoop \
        .current() \
        .start()
