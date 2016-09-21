# coding:utf-8
import json
from StringIO import StringIO

class Data:
    '''
    this is pc json standard
    The json must be have status and data
    status is a str
    data was dict
    '''
    def __init__(self, data = []):
        self.origin = data
        self.data = {}

    def __str__(self):
        '''
        :return:
        '''
        return "json_module"

    def setData(self, key, param):
        '''
        :param key:
        :param param:
        :return:
        '''
        if type(param) in (str, list, dict):
            if key is 'data':
                self.data[key] = param
        return self

    def setStatus(self, key, param):
        '''
        :param key:
        :param param:
        :return:
        '''
        if type(param) in (str, list, dict):
            if key is 'status':
                self.data[key] = param
        return self

    def set(self, key, param):
        '''
        :param key:
        :param param:
        :return:
        '''
        if type(param) in (str, list, dict):
            self.data[key] = param
        return self

    def add(self, key, param):
        '''
        :param key:
        :param param:
        :return:
        '''
        self.data[key].append(param)

    def get(self):
        '''
        :return:
        '''
        return json.dumps(self.data)

    def loads(self, raw_data = ''):
        return json.loads(raw_data)
    
    def to_string(self):
        return json.dumps(self.origin)
