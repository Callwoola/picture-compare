# coding:utf-8
import tornado
import tornado.ioloop
import tornado.web
import tornado.template
from src import (config, routes)
import os


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

    yaml_config = yaml.load(open("./config.yaml"))
    for key in yaml_config.keys():
        # os.environ[key.upper()]=yaml_config[key]
        if not os.environ.has_key(key.upper()):
            os.environ[key.upper()] = str(yaml_config[key])
    pass


config_yaml()

route = routes.getRoutes(config)
application = tornado.web.Application(route)

if __name__ == "__main__":
    # settings = {'debug': True}
    check_self()
    info('config successful ... ')
    application.listen(os.environ[config.PROJECT_PORT])
    application.debug = True
    # application.autoreload=False
    info('Picture-Compare service runing ...')
    tornado \
        .ioloop \
        .IOLoop \
        .current() \
        .start()
