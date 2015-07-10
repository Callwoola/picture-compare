# coding:utf-8
import tornado
import tornado.ioloop
import tornado.web
import tornado.template
from src.controller import demo

PROJECT_DIR = "D:/code/image/"
STATIC_DIR = "img/"
PROJECT_DIR_IMG = PROJECT_DIR + "img/"


def config_yaml():
    '''
    config the App value
    :return:
    '''
    import yaml
    from src import config
    yaml_config=yaml.load(open("./config.yaml"))
    for line in yaml_config:
        if hasattr(config,line.upper()):
            setattr(config,line.upper(),yaml_config[line])
pass


def check_self():
    '''
    check_self config and dependent
    :return:
    '''
    pass

# settings = {'debug': True}
application = tornado.web.Application([
    (r"/", demo.DemoHandler),
    (r"/search", demo.DemoSearchHandler),
    (r"/upload_search", demo.DemoUploadSearchHandler),

    (r'/img/(.*)', tornado.web.StaticFileHandler, {'path': PROJECT_DIR_IMG}),
    (r'/tests/(.*)', tornado.web.StaticFileHandler, {'path': PROJECT_DIR+'/tests'}),
])

if __name__ == "__main__":
    config_yaml()
    application.listen(8888)
    application.debug = True
    # application.autoreload=False
    tornado \
        .ioloop \
        .IOLoop \
        .current() \
        .start()
