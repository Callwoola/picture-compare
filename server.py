# coding:utf-8
import tornado
import tornado.ioloop
import tornado.web
import tornado.template
from src import (config,routes)




def check_self():
    '''
    check_self config and dependent
    :return:
    '''
    pass

def info(str):
    '''
    :param str:
    :return:
    '''
    print str

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
config_yaml()

route=routes.getRoutes(config)
application = tornado.web.Application(route)

if __name__ == "__main__":
    # settings = {'debug': True}
    check_self()
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

