# coding:utf-8
class Image:
    '''
    Compare Image differ  I find some useful function
    Maybe Some function would suit for you Project
    '''
    image_a_path = ""
    image_b_path = ""

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
        imA=Image.open(self.image_a_path)
        imB=Image.open(self.image_b_path)
        if not imA.size is imB.size:
            name="temp."+os.path.basename(self.image_a_path).split('.')[1]
            currentName=os.path.dirname(self.image_a_path)+name
            imB.resize(imA.size).save(currentName)
            self.image_b_path=currentName
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

        return correlate2d(get(self.image_a_path),
                           get(self.image_b_path)).max()


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
        return hamming(a, b)