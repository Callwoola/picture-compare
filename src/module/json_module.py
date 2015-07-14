# coding:utf-8
import src.module.baseModule
import json
from StringIO import StringIO



class baseModule(object):
    def __init__(self):
        print 'base module'
        pass
    pass


class json_module(baseModule):
    '''
    this is pc json standard
    The json must be have status and data
    status is a str
    data was dict
    '''
    def __init__(self):
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
        pass

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
        pass

    def set(self, key, param):
        '''
        :param key:
        :param param:
        :return:
        '''
        if type(param) in (str, list, dict):
            self.data[key] = param
        return self
        pass

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
        print self.data
        return json.dumps(self.data)
        # return io.getvalue()
        # return json
        # pass
