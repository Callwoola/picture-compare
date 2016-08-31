# -*- coding: utf-8 -*-
import tornado
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.template
import json, time, os, uuid
from src.module import json_module
import hashlib
from src import config
from tornado import gen
from tinydb import TinyDB, where


class App(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    def __init__(self):
        super()
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
