# coding:utf-8
import os
import urllib2
import io
import StringIO
from tinydb import TinyDB,where

from PIL import Image as im
from src.lib.data import Data


class Manage:
    image_size = (20,20)

    divided = '--@@--'

    r = None

    def __init__(self, redis = None):
        # 如今已经不需要 redis 的初始化了 叼
        self.r = redis

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
                imgList.append(
                    {
                        "url": package_path + fileName,
                        "path": project_img_path + fileName,
                    }
                )
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
                # print term_key, term_value
                if not condition is None:
                    condition = (where('data').has('data').has(term_key) == term_value) & condition
                else:
                    condition = (where('data').has('data').has(term_key) == term_value)
            list = db.search(condition)
            if len(list) < 10:
                condition = None
                for term_key, term_value in terms.items():
                    # not allow empty condition
                    # print term_key, term_value
                    if not condition is None:
                        condition = (where('data').has('data').has(term_key) == term_value) | condition
                    else:
                        condition = (where('data').has('data').has(term_key) == term_value)
                list = db.search(condition)
        else:
            list = db.all()
        # process result data for reture
        # print condition
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

    # 生成短名称 短名称 在前面
    def __genrate_sort_name(self, names = []):
        '''
        :生成 redis 的 key
        :param keys:
        :return:
        '''
        __sort_dict, __result = {}, {}
        # 根据穷举法, 找到最短的 key
        for s in names:
            for lenght in range(0, len(s)):
                __check_name = s[:(lenght + 1)]
                if not __check_name in __sort_dict.values():
                    # sort name 没有被定义 可以使用
                    __sort_dict[s] = __check_name
                    # 同时进入下一个关键词判断
                    break
        # 首先对names 进行一次排序 保证 每次的结果都一样
        names = sorted(__sort_dict)
        # 重新排序
        for i in names:
            __result[i] = __sort_dict[i]
        return __result

    # ----------------------------------------------------------
    # 生成 redis key 名称
    # ---------------------------------------------------------
    def __generate_key(self, search = [] ,source_data = {}):
        # 生成短名称
        __sort_dict = self.__genrate_sort_name(search)
        if not type(source_data) is dict:
            raise Exception('Keys incorrectness!')

        k_name = ''

        for i in __sort_dict:
            if i in source_data:
                k_name += str(__sort_dict[i]) + '=' + str(source_data[i])
                if __sort_dict.keys()[-1] is not i:
                    k_name += '-'

        return k_name

    # ----------------------------------------------------------
    # 向 redis 创建索引
    # ---------------------------------------------------------
    def index_image(self, id = 0, search = [], data = [], image = '', name = ''):
        # TOOD 需要一个算法 , 将每次 的 search 字段数据 转化为相同的,数据
        # 根据 client 的条件字段创建 的 key
        source_data = {}
        for index_name in search:
            source_data[index_name] = data[index_name]

        # 每个对象必须要有一个名字
        data['name'] = name

        key_name = self.__generate_key(
            search,
            source_data
        )

        # 在尾部加上id
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
                im_instance \
                    .convert('RGB') \
                    .save(output, 'JPEG')

                string = Data(data).to_string()

                value = string + \
                        self.divided + \
                        output.getvalue()

                self.r.set(key_name, value)
            return True
        return False

    base_image_name = 'base_image_name'

    def store_base_image(self, image  = ''):
        res = urllib2.urlopen(image)
        if res.code == 200:
            imimage = io.BytesIO(res.read())
            im_instance = im.open(imimage).resize(self.image_size)
            output = StringIO.StringIO()
            im_instance \
                .convert('RGB') \
                .save(output, 'JPEG')

            self.r.set(self.base_image_name, output.getvalue())

    def store_base_image_file(self, image  = ''):
        im_instance = im.open(image).resize(self.image_size)
        output = StringIO.StringIO()
        im_instance \
            .convert('RGB') \
            .save(output, 'JPEG')

        self.r.set(self.base_image_name, output.getvalue())

    def get_base_image(self):
        result = self.r.get(self.base_image_name)
        return io.BytesIO(result)

    def clear_db(self):
        '''
        : 清除当前数据库
        '''
        print 'clear db ...'
        self.r.flushdb()

    # 单个获取图片
    def get_image(self, key_name = None):
        return io.BytesIO(
            self.r.get(key_name)
        )

    # 单个获取图片
    def get_image_with_data(self, key_name = None):
        data, result = self.r.get(key_name).split(self.divided)
        return data, io.BytesIO(result)

    # ----------------------------------------------------------
    # 根据条件生成数据
    # ---------------------------------------------------------
    def search(self, terms = None):
        # 生成短名称
        if terms:
            key_name = self.__generate_key(
                terms.keys(),
                terms
            )
            print key_name
            return self.r.keys('*' + key_name + '*')
        else:
            return self.r.keys('*')

    def get_multi(self, keys = []):
        if len(keys) > 0:
            return self.r.mget(keys)
        raise Exception('keys is empty!')
