# coding:utf-8
import json
import StringIO
# from src.module import json_module
# from src import config
# from src.adapter import db
import hashlib, time, os

import unittest

from subprocess import call


class TestBaseSearch(unittest.TestCase):
    # def nottest_first(self):
    #     ''' there is processing img and return img list '''
    #     file_path = '/Users/liyang/Code/picture-compare/img/img1/1.jpg'
    #     tmp_name = file_path
    #     terms = []
    #     from src.service.compare import Compare
    #     compareDict = Compare().setCompareImage(tmp_name, terms)
    #     for item in compareDict:
    #         # print call(['imgo '+item['url']])
    #         print call(['id -un'])
    #     self.assertTrue(len(compareDict) > 0)   
    def test_base(self):
        self.assertEqual(True, True)


    def test_module(self):
        print '\n\nstart'
        from src.service.compare import Compare
        file_path = '/Users/liyang/Code/picture-compare/img/img1/1.jpg'
        compareDict = Compare().start(file_path)
        self.assertEqual(True, True)

def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBaseSearch)
    unittest.TextTestRunner(verbosity=2).run(suite)
