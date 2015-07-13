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

    def __init__(self):
        self.data={}

    def __str__(self):
        '''
        :return:
        '''
        return "json_module"

    def set(self,key,param):
        '''
        :param key:
        :param param:
        :return:
        '''
        if type(param) in (str,list,dict):
            self.data[key]=param
        pass
    def add(self,key,param):
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