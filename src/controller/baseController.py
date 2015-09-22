# coding:utf-8

from src.module import json_module

class baseController:

    # set json

    # set input
    def __init__(self):
        pass

    def ok(self, ok):
        if str(ok) == '':
            return None

        return None
    
    def getJson(self):
        pass
    
    def json(self):
        return json_module.json_module()