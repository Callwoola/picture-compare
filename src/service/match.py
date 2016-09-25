# coding:utf-8

from src.lib.data import Data
from src.service.feature import Feature
from src.service.manage import Manage


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

    include_feature = [
#        'start',
        # 'basehash',
        # 'mse',
        # 'perceptualHash',
        # 'colorCompare',
        '_base',
        '_phash',
        '_color',
    ]

    def __init__(self, Manage = None):
        """
        设置 管理器
        """
        self.manage = Manage
        self.feature = Feature()

    
    def set_origin_image(self, image_url = ''):
        # 设置原图片索引
        self.manage.store_base_image(image_url)


    # ----------------------------------------------------------
    # Mixom Hash
    # 混合 hash 算法
    # ----------------------------------------------------------
    def mixHash(self, score_list = {}):
        '''
        :get a mix score
        :return:
        '''
        mse = 0
        phash = 0
        base = 0
        color = 0
        for detector in score_list:
            # if detector is 'Phash':
            #     phash = score_list[detector] * 1000
            if detector is 'Phash':
                phash = score_list[detector] * 1000
            if detector is 'Base':
                phash = score_list[detector] * 1.5
            if detector is 'Mse':
                phash = score_list[detector] * 0.8
            if detector is 'Color':
                phash = score_list[detector] * 1.1

        return (mse + phash + base + color)

    def get_match_result(self, terms = None, limit=10):
        '''
        :param data:
        :return: list | None
        '''

        import time

        the_list = self.manage.search(terms)

        if Manage.base_image_name in the_list:
            the_list.remove(Manage.base_image_name)
        compare = self.feature
        results = []
        print len(the_list)
        bb = time.time()
        for key in the_list:
            # print key
            # 找到比对数据
            compare.set_byte_base_image(
                self.manage.get_base_image()
            )

            data, byte = self.manage.get_image_with_data(key)

            compare.set_byte_storage_image(byte)

            bean = Data().loads(data)


            b = time.time()

            result = {}
            result = compare.process([
                'Phash'
            ])

            score = self.mixHash(result)
            a = time.time()
            
            print 'time:' ,  str(a-b)

            # # 开始比对
            # for feature in self.include_feature:
            #     getattr(compare, feature)()

            # score = compare.mixHash()

            # 准备返回数据
            processed = {}

            for i in bean:
                processed[i] = bean[i]

            processed['id'] = key.split('#')[1]
            processed['score'] = score

            results.append(processed)
        sortedList = sorted(results, key=lambda k: k['score'])
        sortedList = sortedList[:limit]
        item_id = 0

        for i in range(0,len(sortedList)):
            # print results[i]['score']
            sortedList[i]['score'] = item_id
            item_id += 1

        aa = time.time()
        print 'totle time:' ,  str(aa-bb)
        return sortedList

    def setCompareImageBak(self, path=None, terms=None, limit=10, sort="score"):
        '''
        :param data:
        :return: list | None
        '''
        ''' get all image list '''
        # check data is binary file
        try:
            # ------------------------------------------
            # result must got to sort and set size
            # maybe add index for quick find image

            the_list = Manage().get_db_list(terms)
            print the_list
            compare = compareTool.Image()
            results = []
            for bean in the_list:
                
                # --------------------------
                # this is a image buay file
                compare.setA(path)
                if bean['type'] == 'url':
                    compare.setB(bean['map'])
                else:
                    compare.setB(bean['addresses'])

                compare.start()
                # 开始比对
                for feature in self.include_feature:
                    getattr(compare, feature)()

                score = compare.mixHash()
                results.append({
                    # 'score_basehash': compare.basehash(),
                    'score': score,
                    # 'score_image': compare.mse(),
                    'url': '' if bean['type'] != 'url' else bean['addresses'],
                    'id': bean['id'],
                    'data': bean['data'],
                    'name': bean['name'],
                })
            sortedList = sorted(results, key=lambda k: k['score'])
            sortedList = sortedList[:limit]
            item_id = 0
            for i in range(0,len(sortedList)):
                # print results[i]['score']
                sortedList[i]['score']=item_id
                item_id+=1
            return sortedList
        except Exception, e:
            print e
        return None


    # def start(
    #     self,
    #     path=None,
    #     terms=None,
    #     limit=10,
    #     sort="score"
    # ):
    #     try:
    #         print 'im here'
    #         the_list = Manage().get_db_list(terms)
    #         compare = compareTool.Image()
    #         results = []
    #         for bean in the_list:
    #             compare.setA(path)
    #             if bean['type'] == 'url':
    #                 compare.setB(bean['map'])
    #             else:
    #                 compare.setB(bean['addresses'])
    #             compare.start()
    #             for feature in self.include_feature:
    #                 getattr(compare, feature)()
    #             score = compare.mixHash()
    #             results.append({
    #                 'score': score,
    #                 'url': '' if bean['type'] != 'url' else bean['addresses'],
    #                 'id': bean['id'],
    #                 'data': bean['data'],
    #                 'name': bean['name'],
    #             })
    #         sortedList = sorted(results, key=lambda k: k['score'])
    #         sortedList = sortedList[:limit]

    #         # print sortedList
    #         # print len(sortedList)
    #         # exit()
    #         if not len(sortedList) > 0:
    #             raise Exception('Not match any image!')
    #         item_id = 0
    #         for i in range(0,len(sortedList)):
    #             sortedList[i]['score']=item_id
    #             item_id+=1
    #         return sortedList
        
    #     except Exception, e:
    #         print e
    #     return None


    
    # def getAllList(self):
    #     # os path
    #     pass
