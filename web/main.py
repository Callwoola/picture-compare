# coding:utf-8
import lib.Image

import tornado
import tornado.ioloop
import tornado.web
import jinja2
import tornado.template
# from template import tornado


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader("./")
        html = loader.load("index.html").generate(myvalue="XXX")
        print lib.Image.image.gettest()
        print "asdf"
        # t = tornado.template.Template("<html>{{ myvalue }}</html>")
        self.write(html)


#settings = {'debug': True}
application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    application.debug=True
    #application.autoreload=False

    tornado.ioloop.IOLoop.current().start()

    # server = tornado.httpserver.HTTPServer(application)
    # server.listen(8888)
    # instance = tornado.ioloop.IOLoop.instance()
    # tornado.autoreload.start(instance)
    # instance.start()
