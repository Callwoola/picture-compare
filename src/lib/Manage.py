# coding:utf-8

from tinydb import TinyDB,where
from src import config
import os


class Manage:
    def __init__(self):
        pass

    
    def all(self):
        db = TinyDB(os.environ[config.STORAGE_INDEX_DB])
        return db.all()
    
    # ----------------------------------------------------------
    # get directory file list
    # ----------------------------------------------------------
    def getImageList(self, project_img_path, package_path):
        '''
        :param project_img_path:
        :param package_path:
        :return:
        '''
        import os

        imgList = []
        for dir_, _, files in os.walk(project_img_path):
            for fileName in files:
                imgList.append({"url": package_path + fileName,
                                "path": project_img_path + fileName,
                                })
        return imgList

    # ----------------------------------------------------------
    # return the package first file name
    # ----------------------------------------------------------
    def getFirst(self, project_img_path):
        '''
        :param project_img_path:
        :return:
        '''
        import os

        for dir_, _, files in os.walk(project_img_path):
            for fileName in files:
                return fileName
        return None

    # ----------------------------------------------------------
    # return path all file pull path name
    # ---------------------------------------------------------
    def getPathAllFile(self, PATH):
        '''
        :param PATH:
        :return:
        '''
        import os, glob

        pathList = []
        os.chdir(PATH)
        for i in glob.glob('*'):
            pathList.append(os.getcwd() + "/" + i)
        return pathList

    def add_index_file(self, json, data):
        # if data ta
        pass

    # ----------------------------------------------------------
    # return Tinydb all list
    # ---------------------------------------------------------
    def get_db_list(self, terms=None, PATH=None):
        '''
        :param PATH:
        :return:
        '''
        db = TinyDB(os.environ[config.STORAGE_INDEX_DB])
        list = []
        # multipul condition
        if len(terms) > 0:
            condition = None
            for term_key, term_value in terms.items():
                # not allow empty condition
                if not condition is None:
                    condition = (where('data').has('data').has(term_key) == term_value) | condition
                else:
                    condition = (where('data').has('data').has(term_key) == term_value)
            list = db.search(condition)
        else:
            list = db.all()
        # process result data for reture
        results = []
        for i in list:
            results.append(
                {
                    'name': i['data']['name'],
                    'map': i['data']['map'],
                    'selfid': i['id'],
                    'id': i['data']['id'],
                    'addresses': i['data']['url'],
                    'type': 'url',
                    'data': i['data']['data']
                }
            )
        return results

        #
        # the_list.append(
        #     {
        #         'name': 'the1',
        #         'addresses': 'http://localhost:8888/img/img1/2.jpg',
        #         'id': 'the2',
        #         'type': 'url',
        #         'map': 'D:/code/image/img/img1/2.jpg',
        #     }
        # )
        # the_list.append(
        #     {
        #         'name': 'the1',
        #         'addresses': 'http://localhost:8888/img/img1/3.jpg',
        #         'id': 'the3',
        #         'type': 'url',
        #         'map': 'D:/code/image/img/img1/3.jpg',
        #     }
        # )
