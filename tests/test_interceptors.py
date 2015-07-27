import base64
import logging
import logging.config
import tornado.httpserver
import tornado.ioloop
import tornado.web

log = logging.getLogger("root")


def interceptor(func):
    """
    This is a class decorator which is helpful in configuring
    one or more interceptors which are able to intercept, inspect,
    process and approve or reject further processing of the request
    """

    def classwrapper(cls):
        def wrapper(old):
            def inner(self, transforms, *args, **kwargs):
                print self.request
                print old
                return old(self, transforms, *args, **kwargs)
            return inner
        cls._execute = wrapper(cls._execute)
        return cls
    return classwrapper


@interceptor("func-")
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, interceptor")


application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(3232)
    tornado.ioloop.IOLoop.instance().start()

