# coding:utf-8

from PIL import Image as im
from src.detector import Detector

class Phash(Detector):

    def calculate(self, origin = None, local = None):
        # 注册 执行 perceptual hash
        return self._phash(origin, local)

    # ----------------------------------------------------------
    # perceptual Hash
    # very quick 8 x 8
    # 感知 hash 算法 , 通过指纹匹配
    # ----------------------------------------------------------
    def _phash(self, origin = None, local = None):
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

        # a = avhash(self.byte_base, im)
        # b = avhash(self.byte_storage, im)

        # a 需要 静态化
        if self._base_image is None:
            print 'calculate again'
            self._base_image = avhash(origin, im)

        b = avhash(local, im)
        value = hamming(self._base_image, b)
        # self.value_of_perceptualHash = value

        return value
