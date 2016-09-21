# coding:utf-8
import os
import urllib2
import io
import redis
import StringIO
from tinydb import TinyDB,where
from src import config
from PIL import Image as im
from src.service.data import Data

class Manage:
    image_size = (100,100)

    divided = '--@@--'

    r = None
    
    def __init__(self):
        # config redis connection server
        self.r = redis.StrictRedis(host='192.168.10.10')

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
                imgList.append({
                    "url": package_path + fileName,
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
                print term_key, term_value
                if not condition is None:
                    condition = (where('data').has('data').has(term_key) == term_value) & condition
                else:
                    condition = (where('data').has('data').has(term_key) == term_value)
            list = db.search(condition)
            if len(list) < 10:
                condition = None
                for term_key, term_value in terms.items():
                    # not allow empty condition
                    print term_key, term_value
                    if not condition is None:
                        condition = (where('data').has('data').has(term_key) == term_value) | condition
                    else:
                        condition = (where('data').has('data').has(term_key) == term_value)
                list = db.search(condition)
        else:
            list = db.all()
        # process result data for reture
        print condition
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

    def __generate_key(self, search = [] ,keys = {}):
        '''
        :生成 redis 的 key
        :param keys:
        :return:
        '''
        if type(keys) is dict:
            k_name = ''
            for k in keys:
                k_name += k + ':' + str(keys[k])
                if keys.keys()[-1] is not k:
                    k_name += '-'
            return k_name, binding_keys
        raise Exception('Keys incorrectness!')

    def index_image(self, id = 0, search = [], condition = {}, data = [], image = ''):
        # 根据 client 的条件字段创建 的 key
        key_name, binding_keys  = self.__generate_key(
            search,
            condition
        )

        # TODO 
        
        key_name += '#' + str(id)
        # 0 -> data
        # 1 -> image - binary
        if image:
            res = urllib2.urlopen(image)
            if res.code == 200:
                # save data into Bytes
                imimage = io.BytesIO(res.read())
                # 压缩图片以及,格式化为 JPEG
                im_instance = im.open(imimage).resize(self.image_size)
                output = StringIO.StringIO()
                im_instance.save(output, 'JPEG')
                # data + output.getvalue()
                string = Data(data).to_string()

                value = string + \
                        self.divided + \
                        output.getvalue()

                self.r.set(key_name, value)
            return True
        return False
