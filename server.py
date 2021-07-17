# coding:utf-8
import os
import yaml
import redis
import tornado
import tornado.web
import tornado.template
import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import define, options
from tornado.ioloop import IOLoop

from src import routes

def config_yaml():
    '''
    config the App value
    :return:
    '''
    yaml_config = yaml.load(open("./config.yaml"))
    # 全局可用变量
    # config = yaml_config
    if not 'redis' in yaml_config.keys():
        raise Exception('config error not redis config')
    if not 'port' in yaml_config.keys():
        raise Exception('config error not port key')
    if not 'binding_host' in yaml_config.keys():
        raise Exception('config error not binding_host key')
    if not 'result_size' in yaml_config.keys():
        raise Exception('config error not result_size key')
    # 做检查
    return yaml_config

config = config_yaml()

class Application(tornado.web.Application):
    def __init__(self):
        ''' the setting '''
        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__), "src/template"),
            static_path = os.path.join(os.path.dirname(__file__), "src/static"),
            # autoreload=False,
            # debug=False,
            autoreload = True,
            debug = True,
        )

        self.config = config
        route = routes.getRoutes(config)
        
        _host = self.config['redis']['host']
        _port = self.config['redis']['port']
        _db = self.config['redis']['db']
        # 需要认真阅读这里的文章
        # https://mirrors.segmentfault.com/itt2zh/ch4.html
        self.r = redis.Redis(
            host = _host,
            port = _port,
            db = _db
        )

        # 初始化  redis 
        # 服务器初始化
        tornado.web.Application.__init__(self, handlers=route, **settings)

# start run
def main():
    # 服务启动的进程
    num_processes = 1
    app_port = config['port']
    address = config['binding_host']
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())

    # listen 可以显式创建创建 http
    # http_server.listen(app_port)
    http_server.bind(app_port)
    http_server.start(num_processes)
    # IOLoop.current().start()
    IOLoop.instance().start()

# main run
if __name__ == "__main__":
    main()      
