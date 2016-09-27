# coding:utf-8
import os
import redis
import tornado
import tornado.web
import tornado.template
import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import define, options
from tornado.ioloop import IOLoop


from src import (config, routes)
def config_yaml():
    '''
    config the App value
    :return:
    '''
    import yaml

    yaml_config = yaml.load(open("./config.yaml"))
    # 全局可用变量
    # config = yaml_config
    
    for key in yaml_config.keys():
        # os.environ[key.upper()]=yaml_config[key]
        if not os.environ.has_key(key.upper()):
            os.environ[key.upper()] = str(yaml_config[key])
            if key == "project_dir":
                os.environ[key.upper()] = os.getcwd() + "/"
            if key == "storage_index_db":
                os.environ[key.upper()] = os.getcwd() + "/" + str(yaml_config[key])
            if key == "template":
                os.environ[key.upper()] = os.getcwd() + "/" + str(yaml_config[key])


config_yaml()

route = routes.getRoutes(config)


class Application(tornado.web.Application):
    def __init__(self):
        # urls settings
        # handlers = 
        ''' the setting '''
        # settings = dict(
        #     template_path=os.path.join(os.path.dirname(__file__), "webapp/templates"),
        #     static_path=os.path.join(os.path.dirname(__file__), "webapp/static"),
        #     # 防跨站伪造请求
        #     xsrf_cookies=False,
        #     cookie_secret="test-2001",
        #     login_url="/login",
        #     # 调试模式
        #     debug=True,
        # )
        settings = dict(
            autoreload=False,
            debug=False
        )
        # settings = dict(
        #     autoreload=True,
        #     debug=True
        # )

        _host = '192.168.10.10' #os.environ[config.REDIS]['host']
        _port = '6379' #os.environ[config.REDIS]['port']
        _db = 1 #os.environ[config.REDIS]['db']
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
    app_port = 5555

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())

    # listen 可以显式创建创建 http
    # http_server.listen(app_port)
    http_server.bind(app_port)
    http_server.start(num_processes)
    IOLoop.current().start()
    # IOLoop.instance().start()

# main run
if __name__ == "__main__":
    main()      
