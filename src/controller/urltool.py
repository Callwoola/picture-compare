# coding:utf-8
import tornado
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.template
import json, time, os, uuid
from src.module import json_module
import hashlib
from src import config

# from tornado import queues
from tornado import gen

from tinydb import TinyDB, where




class urltoolHandler(tornado.web.RequestHandler):
    def get(self, type=None):
        # self.set_header('Content-Type', 'application/json')
        self.write('''
<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE cross-domain-policy SYSTEM "http://www.macromedia.com/xml/dtds/cross-domain-policy.dtd">
<cross-domain-policy>
    <allow-access-from domain="*" />
</cross-domain-policy>
        ''')
