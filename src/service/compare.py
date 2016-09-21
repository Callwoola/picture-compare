# coding:utf-8

from src.lib import Compare as compareTool
from src.lib.Manage import Manage

class Compare:
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
        'basehash',
        'mse',
        'perceptualHash',
        'colorCompare',
    ]

    def __init__(self):
        pass

    def setCompareImage(self, path=None, terms=None, limit=10, sort="score"):
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
                for feature in self.include_feature:
                    getattr(compare, feature)()
                # compare.basehash()
                # compare.mse()
                # compare.perceptualHash()
                # compare.colorCompare()

                score = compare.mixHash()
                # print score
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


    def start(
        self,
        path=None,
        terms=None,
        limit=10,
        sort="score"
    ):
        try:
            print 'im here'
            the_list = Manage().get_db_list(terms)
            compare = compareTool.Image()
            results = []
            for bean in the_list:
                compare.setA(path)
                if bean['type'] == 'url':
                    compare.setB(bean['map'])
                else:
                    compare.setB(bean['addresses'])
                compare.start()
                for feature in self.include_feature:
                    getattr(compare, feature)()
                score = compare.mixHash()
                results.append({
                    'score': score,
                    'url': '' if bean['type'] != 'url' else bean['addresses'],
                    'id': bean['id'],
                    'data': bean['data'],
                    'name': bean['name'],
                })
            sortedList = sorted(results, key=lambda k: k['score'])
            sortedList = sortedList[:limit]

            # print sortedList
            # print len(sortedList)
            # exit()
            if not len(sortedList) > 0:
                raise Exception('Not match any image!')
            item_id = 0
            for i in range(0,len(sortedList)):
                sortedList[i]['score']=item_id
                item_id+=1
            return sortedList
        
        except Exception, e:
            print e
        return None


    
    def getAllList(self):
        # os path
        pass
