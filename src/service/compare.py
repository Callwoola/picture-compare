# coding:utf-8

from src.lib import Compare as compareTool


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

    def __init__(self):
        pass

    def setCompareImage(self, path=None, sort="score"):
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
            from src.lib.Manage import Manage

            the_list = Manage().get_db_list()

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

                results.append({
                    # 'score_basehash': compare.basehash(),
                    'score': compare.basehash(),
                    # 'score_image': compare.mse(),
                    'url': '' if bean['type'] != 'url' else bean['addresses'],
                    'id': bean['id'],
                })
            return sorted(results, key=lambda k: k[sort])
        except Exception, e:
            print e
        return None

    def getAllList(self):

        pass
