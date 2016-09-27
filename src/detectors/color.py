# coding:utf-8

from PIL import Image as im
from src.detector import Detector

class Phash(Detector):

    def calculate(self, origin = None, local = None):
        # 注册 执行 perceptual hash
        return self._mse(origin, local)

    # ----------------------------------------------------------
    # color compare
    # 
    # ----------------------------------------------------------
    def _color(self, RGB_A=None, RGB_B=None):
        '''
        计算两个三维向量距离
        （R1-R2)^2   +   (G1-G2)^2   +   (B1-B2)^2   的值的平方根，即颜色空间的距离
        距离越大，差距就越大。
        :return:
        '''
        def getRgb(io):
            r, g, b = im.open(io).convert('RGB').resize((1, 1)).getcolors()[0][1]
            return [r, g, b]

        if RGB_A is None and RGB_B is None:
            RGB_A = getRgb(self.byte_base)
            RGB_B = getRgb(self.byte_storage)
        if len(RGB_A) == 3 and len(RGB_B) == 3:
            score = (RGB_A[0] - RGB_B[0]) ** 2 + (RGB_A[1] - RGB_B[1]) ** 2 + (RGB_A[2] - RGB_B[2]) ** 2
            self.value_of_colorCompare = abs(score)
            return abs(score)
        self.value_of_colorCompare = 0
        return False

    # ----------------------------------------------------------
    # color compare
    # 
    # ----------------------------------------------------------
    def colorCompare(self, RGB_A=None, RGB_B=None):
        '''
        计算两个三维向量距离
        （R1-R2)^2   +   (G1-G2)^2   +   (B1-B2)^2   的值的平方根，即颜色空间的距离
        距离越大，差距就越大。
        :return:
        '''
        from PIL import Image as im

        def getRgb(path):
            r, g, b = im.open(path).convert('RGB').resize((1, 1)).getcolors()[0][1]
            return [r, g, b]

        if RGB_A is None and RGB_B is None:
            RGB_A = getRgb(self.image_a_path)
            RGB_B = getRgb(self.image_b_path)
        if len(RGB_A) == 3 and len(RGB_B) == 3:
            score = (RGB_A[0] - RGB_B[0]) ** 2 + (RGB_A[1] - RGB_B[1]) ** 2 + (RGB_A[2] - RGB_B[2]) ** 2
            self.value_of_colorCompare = abs(score)
            return abs(score)
        self.value_of_colorCompare = 0
        return False

    def colorTriangleCompare(self):
        '''
        计算两个三维向量的夹角
        l1=sqrt(r1*r1+g1*g1+b1*b1);
        l2=sqrt(r2*r2+g2*g2+b2*b2);
        cos(a)=(r1*r2+g1*g2+b1*b2)/(l1*l2);
        :return:
        '''
        from PIL import Image as im

        def getRgb(path):
            r, g, b = im.open(path).convert('RGB').resize((1, 1)).getcolors()[0][1]
            return [r, g, b]

        #
        # RGB_A = getRgb(self.image_a_path)
        # RGB_B = getRgb(self.image_b_path)
        # l1=sqrt(r1*r1+g1*g1+b1*b1)
        # l2=sqrt(r2*r2+g2*g2+b2*b2)
        # cos(a)=(r1*r2+g1*g2+b1*b2)/(l1*l2)
        return

        def findSameColor(self, rgb=None, all=None):
        '''
        :return:
        '''
        from src.lib.image import Image
        # from PIL import Image as im
        rgbList = Image.rgb_list
        def getRgb(path):
            r, g, b = im.open(path).convert('RGB').resize((1, 1)).getcolors()[0][1]
            return (r, g, b)

        theList = []
        if rgb is None:
            origin_Rgb = getRgb(self.image_a_path)
        else:
            origin_Rgb = rgb

        def score(RGB_A, RGB_B):
            # print '------------------------'
            # print RGB_A
            # print RGB_B
            score = (RGB_A[0] - RGB_B[0]) ** 2 + (RGB_A[1] - RGB_B[1]) ** 2 + (RGB_A[2] - RGB_B[2]) ** 2
            # print  abs(score)
            return score

        for i in rgbList:
            key = i.keys()[0]
            value = i[i.keys()[0]]
            theList.append({
                'score': score(origin_Rgb, value),
                'keyname': key,
                'rgb': "rgb(%d , %d ,%d)" % value
            })
        # results = sorted(theList, key=lambda k: k['score'], reverse=True)
        results = theList
        if all is True:
            return results
        return results[0]

    def find12colorList(self, rgb=None, all=None):
        '''
        :return:
        '''
        from src.module.color_module import rgb12List
        from PIL import Image as im

        def getRgb(path):
            r, g, b = im.open(path).convert('RGB').resize((1, 1)).getcolors()[0][1]
            return (r, g, b)

        theList = []
        if rgb is None:
            origin_Rgb = getRgb(self.image_a_path)
        else:
            origin_Rgb = rgb

        def score(RGB_A, RGB_B):
            # print '------------------------'
            # print RGB_A
            # print RGB_B
            score = (RGB_A[0] - RGB_B[0]) ** 2 + (RGB_A[1] - RGB_B[1]) ** 2 + (RGB_A[2] - RGB_B[2]) ** 2
            # print  abs(score)
            return abs(score)

        for k, v in rgb12List.iteritems():
            theList.append({
                'score': score(origin_Rgb, v),
                'keyname': k,
                'rgb': "rgb(%d , %d ,%d)" % v
            })
        # results = sorted(theList, key=lambda k: k['score'], reverse=True)
        results = theList
        if all is True:
            return results
        return results[0]


