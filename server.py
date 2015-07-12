# coding:utf-8
import tornado
import tornado.ioloop
import tornado.web
import tornado.template
from src.controller import demo
from src.controller import search
from src import config


def config_yaml():
    '''
    config the App value
    :return:
    '''
    import yaml
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
def info(str):
    print str
# settings = {'debug': True}
config_yaml()
application = tornado.web.Application([
    (r"/", demo.DemoHandler),
    (r"/search", demo.DemoSearchHandler),
    (r"/upload_search", demo.DemoUploadSearchHandler),

    (r'/img/(.*)', tornado.web.StaticFileHandler, {'path': config.STATIC_DIR}),
    #(r'/tests/(.*)', tornado.web.StaticFileHandler, {'path': config.PROJECT_DIR+'/t}),



    #---------------------------------------------
    (r'/_search/json/(.*)', search.JsonHandler),
])

if __name__ == "__main__":

    info('config successful ... ')
    application.listen(8888)
    application.debug = True
    # application.autoreload=False
    info('Picture-Compare service runing ...')
    tornado \
        .ioloop \
        .IOLoop \
        .current() \
        .start()

