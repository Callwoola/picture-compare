# coding:utf-8

import io
import json
from src.lib.data import Data
from src.service.feature import Feature
from src.service.manage import Manage
import multiprocessing as mp
from multiprocessing import Pool
from functools import partial

def mix_hash(score_list = {}):
    '''
    : merge image score
    '''
    mse = 0
    phash = 0
    base = 0
    color = 0
    for detector in score_list:
        if detector is 'Phash':
            phash = score_list[detector] * 1000
        if detector is 'Base':
            base = score_list[detector] * 1.5
        if detector is 'Mse':
            mse = score_list[detector] * 0.8
        if detector is 'Color':
            color = score_list[detector] * 1.1

    return (mse + phash + base + color)


def process_match(origin_io=None, lists=None):
    '''
    : match image by different process
    '''
    feature = Feature()
    data = Data()

    # print lists
    results = []

    # 直接返回 redis row data
    for container in lists:
        # 找到比对数据
        feature.set_byte_base_image(origin_io)

        # 风格数据
        data, image_str = container.split(Manage.divided)

        byte = io.BytesIO(image_str)
        feature.set_byte_storage_image(byte)

        bean = json.loads(data)
        result = {}
        # 使用算法到的
        result = feature.process([
            'Phash'
        ])

        # merge calculate score
        score = mix_hash(result)
        # 准备返回数据
        processed = {}

        for i in bean:
            processed[i] = bean[i]
        processed['score'] = score

        results.append(processed)
    return results

class Match:
    '''
    Compare Image differ  I find some useful function
    Maybe Some function would suit for you Project
    '''
    image_a_path = ""
    image_b_path = ""

    value_of_phash = None
    value_of_mse = None
    value_of_perceptualHash = None

    # 原对比文件 的 byte 属性
    origin_io_image = None

    def __init__(self, Manage = None, result_size = 10):
        """
        设置 管理器
        """
        self.manage = Manage
        self.feature = Feature()
        self.data = Data()
        self.result_size = result_size
        self.origin_io_image = self.manage.get_base_image()

    def set_origin_image(self, image_url = ''):
        # 设置原图片索引
        if image_url is '':
            raise Exception('Origin image is empty')
        self.manage.store_base_image(image_url)

    def get_match_result(self, terms = None):
        '''
        :param data:
        :return: list | None
        '''

        limit = self.result_size
        the_list = self.manage.search(terms)
        if Manage.base_image_name in the_list:
            the_list.remove(Manage.base_image_name)

        for_multiprocess_list = []
        for_multiprocess_list = self.manage.get_multi(the_list)

        print 'count result:', str(len(the_list))

        results = []
        core_number = mp.cpu_count()

        # 计算每个 cpu 需要的数量 (分化数据到每个 cpu )
        n = int(round(len(for_multiprocess_list) / float(core_number)))
        divid_list = [for_multiprocess_list[i:i + n] for i in xrange(0, len(for_multiprocess_list), n)]


        # Pool的默认大小是CPU
        pool = Pool()
        func = partial(process_match, self.origin_io_image)

        # 并得到合并的结果集
        rl = pool.map(func, divid_list)
        pool.close()
        pool.join()

        # set two dimension to one dimension
        results = [item for i in rl for item in i]

        sortedList = sorted(results, key=lambda k: k['score'])
        sortedList = sortedList[:limit]
        item_id = 0

        return sortedList
