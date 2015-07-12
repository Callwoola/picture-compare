# coding:utf-8
class Image:
    '''
    Compare Image differ  I find some useful function
    Maybe Some function would suit for you Project
    '''
    image_a_path = ""
    image_b_path = ""

    value_of_phash = None
    value_of_mse = None
    value_of_perceptualHash = None

    def __init__(self, A=None, B=None):
        # image A is String of path
        # image B is String of path
        pass

    def setA(self, path):
        self.image_b_path = path

    pass

    def setB(self, path):
        self.image_a_path = path

    pass

    def start(self):
        import os
        from PIL import Image

        imA = Image.open(self.image_a_path)
        imB = Image.open(self.image_b_path)
        if not imA.size is imB.size:
            name = "temp." + os.path.basename(self.image_a_path).split('.')[1]
            currentName = os.path.dirname(self.image_a_path) + name
            imB.resize(imA.size).save(currentName)
            self.image_b_path = currentName
        pass

    def end(self):
        import os

        os.remove(self.image_b_path)
        pass

    # ----------------------------------------------------------
    # mse
    #
    # return int
    # return the MSE, the lower the error, the more "similar"
    # NOTE: the two images must have the same dimension
    # ----------------------------------------------------------
    def mse(self):
        """
        :return: float
        """
        import numpy as np
        import cv2

        imageA = cv2.imread(self.image_a_path)
        imageB = cv2.imread(self.image_b_path)

        imageA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        imageB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])
        self.value_of_mse = err
        return err

    # ----------------------------------------------------------
    # base
    #
    # return int
    # return the MSE, the lower the error, the more "similar"
    # NOTE: the two images must have the same dimension
    # ----------------------------------------------------------
    def phash(self):
        """phash compare If histogram smooth
        :return: float
        """
        import math
        import operator
        from PIL import Image

        image1 = Image.open(self.image_a_path)
        image2 = Image.open(self.image_b_path)

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
        """So fucking slow
        :return: float
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
    # ----------------------------------------------------------
    def perceptualHash(self):
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
    # mix Hash
    # ----------------------------------------------------------
    def mixHash(self):
        '''
        get a mix score
        :return:
        '''
        if not self.value_of_mse is None and \
                not self.value_of_perceptualHash is None and \
                not self.value_of_phash is None:
            return self.value_of_perceptualHash * 1000 + \
                   self.value_of_phash * 1.5 + \
                   self.value_of_mse * 0.8
        return None
        # --------------------
        # waiting ...
        # color value
        pass

    # ----------------------------------------------------------
    # color compare
    # ----------------------------------------------------------
    def colorCompare(self):
        '''
        :return:
        '''

        '''
        计算两个三维向量距离
        （R1-R2)^2   +   (G1-G2)^2   +   (B1-B2)^2   的值的平方根，即颜色空间的距离
        距离越大，差距就越大。

        '''
        from PIL import Image as im

        def getRgb(path):
            r, g, b = im.open(path).convert('RGB').resize((1, 1)).getcolors()[0][1]
            return [r, g, b]

        RGB_A = getRgb(self.image_a_path)
        RGB_B = getRgb(self.image_b_path)

        score= (RGB_A[0] - RGB_B[0]) ^ 2 + (RGB_A[1] - RGB_B[1]) ^ 2 + (RGB_A[2] - RGB_B[2]) ^ 2
        print score
        return score
        # from src.module.RGB_module import RGB_module
        # rgb1 = RGB_module(self.image_a_path).get()
        # print rgb1
        # print
        return None


    def colorTriangleCompare(self):
        '''
        计算两个三维向量的夹角
        l1=sqrt(r1*r1+g1*g1+b1*b1);
        l2=sqrt(r2*r2+g2*g2+b2*b2);
        cos(a)=(r1*r2+g1*g2+b1*b2)/(l1*l2);
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