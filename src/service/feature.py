# coding:utf-8
import math
import operator
from PIL import Image as im
from src.detectors.phash import Phash

# 方向 base 的数据其实只需要提取一次啊, 囧~~
class Feature:
    '''
    Compare Image differ  I find some useful function
    Maybe Some function would suit for you Project
    '''
    image_a_path = ""
    image_b_path = ""

    value_of_phash = None
    value_of_mse = None
    value_of_perceptualHash = None
    value_of_colorCompare = None

    image_a_binary = None
    image_b_binary = None


    detector = {}
    
    def __init__(self):        
        self.__reg(Phash())


    def __reg(self, instance_name = None):
        self.detector[
            instance_name.get_name()
        ] = instance_name

    def process(self, detector_list = []):
        result = {}

        for i in self.detector:
            if i in detector_list:
                result[i] = self.detector[i].calculate(
                    self.byte_base,
                    self.byte_storage
                )

        return result

    # 使用比特码对比
    byte_base = None
    byte_storage = None

    # 算法特征
    # 将原对比图片 预先出错 , 避免 重复计算
    base_image_trait_for_image = None
    base_image_trait_for_cv = None    

    def set_byte_base_image(self, byte):
        self.byte_base = byte

    def set_byte_storage_image(self, byte):
        self.byte_storage = byte        

    def setA(self, path):
        self.image_b_path = path


    def setB(self, path):
        self.image_a_path = path


        
    def set_a_source(self, data):
        ''' set a binary variable
        :param data:
        :return:
        '''
        self.image_a_binary = data
        return self

    def set_b_source(self, data):
        ''' set a binary variable
        :param data:
        :return:
        '''
        self.image_b_binary = data
        return self

    def start(self):
        import os
        from PIL import Image
        # print 'start - compare'
        imA = Image.open(self.image_a_path)
        imB = Image.open(self.image_b_path)
        if not imA.size is imB.size:
            name = "temp." + os.path.basename(self.image_a_path).split('.')[1]
            currentName = os.path.dirname(self.image_a_path) + name
            imB.resize(imA.size).save(currentName)
            self.image_b_path = currentName

    def end(self):
        import os
        os.remove(self.image_b_path)

    # ----------------------------------------------------------
    # mse 均方误差
    # MSE可以评价数据的变化程度，MSE的值越小，说明预测模型描述实验数据具有更好的精确度。与此相对应的，还有均方根误差RMSE、平均绝对百分误差等等。
    # ----------------------------------------------------------
    def mse(self, path=True):
        """
        :return: float
        """
        import numpy as np
        import cv2

        # 使用 io byte 读取数据
        # import numpy as np
        # a1=io.BytesIO(rr.get('base_image_name'))
        # nparr = np.fromstring(a1.read(), np.uint8)
        # img_np = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)
        # cv2.imshow('image',img_np)
        # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        # cv2.imshow('image',img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        if path:
            imageA = cv2.imread(self.image_a_path)
            imageB = cv2.imread(self.image_b_path)
        else:
            imageA = cv2.imread(self.image_a_binary)
            imageB = cv2.imread(self.image_b_binary)
        imageA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        imageB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])
        self.value_of_mse = err
        return err

    # ----------------------------------------------------------
    # base
    # 算法 -> 直方图比较
    # ----------------------------------------------------------
    def basehash(self, path=True):
        """basehash compare If histogram smooth
        :return: float
        """

        if path:
            image1 = im.open(self.image_a_path)
            image2 = im.open(self.image_b_path)
        else:
            image1 = im.open(self.image_a_binary)
            image2 = im.open(self.image_b_binary)

        if not image1.size is image2.size:
            image2 = image2.resize(image1.size)
        pass
        h1 = image1.convert('RGB').histogram()
        h2 = image2.convert('RGB').histogram()

        rms = math.sqrt(
            reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2)))
            /
            len(h1)
        )
        self.value_of_phash = rms
        return rms

    
    # ----------------------------------------------------------
    # correlate2d
    # very slow
    # return int
    # return the MSE, the lower the error, the more "similar"
    # NOTE: the two images must have the same dimension
    # ----------------------------------------------------------
    def correlate2d(self):
        """
        : So fucking slow
        : return: float
        """
        import scipy as sp
        from scipy.misc import imread
        from scipy.signal.signaltools import correlate2d

        def get(path):
            data = imread(path)
            data = sp.inner(data, [299, 587, 114]) / 1000.0
            return (data - data.mean()) / data.std()

        value = correlate2d(get(self.image_a_path),
                            get(self.image_b_path)).max()
        return value

    # ----------------------------------------------------------
    # perceptual Hash
    # very quick 8 x 8
    # 感知 hash 算法 , 通过指纹匹配
    # ----------------------------------------------------------
    def perceptualHash(self, path=True):
        '''
        huhh...
        '''
        from PIL import Image

        def avhash(im):
            if not isinstance(im, Image.Image):
                im = Image.open(im)
            im = im.resize((8, 8), Image.ANTIALIAS).convert('L')
            avg = reduce(lambda x, y: x + y, im.getdata()) / 64.
            return reduce(lambda x, (y, z): x | (z << y),
                          enumerate(map(lambda i: 0 if i < avg else 1, im.getdata())),
                          0)
        # 汗明距离
        def hamming(h1, h2):
            h, d = 0, h1 ^ h2
            while d:
                h += 1
                d &= d - 1
            return h

        a = avhash(self.image_a_path)
        b = avhash(self.image_b_path)
        value = hamming(a, b)
        self.value_of_perceptualHash = value
        return value

    # ----------------------------------------------------------
    # perceptual Hash
    # very quick 8 x 8
    # 感知 hash 算法 , 通过指纹匹配
    # ----------------------------------------------------------
    def _phash(self):
        def avhash(io, im):
            # print im
            # print im
            # if not isinstance(im, Image.Image):
            the_image = im.open(io)
            the_image = the_image.resize((8, 8), im.ANTIALIAS).convert('L')
            avg = reduce(lambda x, y: x + y, the_image.getdata()) / 64.
            return reduce(
                lambda x, (y, z): x | (z << y),
                enumerate(map(lambda i: 0 if i < avg else 1, the_image.getdata())),
                0
            )

        # 汗明距离
        def hamming(h1, h2):
            h, d = 0, h1 ^ h2
            while d:
                h += 1
                d &= d - 1
            return h

        a = avhash(self.byte_base, im)
        b = avhash(self.byte_storage, im)
        value = hamming(a, b)
        self.value_of_perceptualHash = value
        return value

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

        pass

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
