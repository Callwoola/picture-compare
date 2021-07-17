# coding:utf-8

from PIL import Image as im
from src.detector import Detector

class Color(Detector):

    def calculate(self, origin = None, local = None):
        # 注册 执行 perceptual hash
        return self._color(origin, local)

    # ----------------------------------------------------------
    # color compare
    # 
    # ----------------------------------------------------------
    def _color(self, origin=None, local=None):
        '''
        计算两个三维向量距离
        （R1-R2)^2   +   (G1-G2)^2   +   (B1-B2)^2   的值的平方根，即颜色空间的距离
        距离越大，差距就越大。
        :return:
        '''
        def getRgb(io):
            r, g, b = im.open(io).convert('RGB').resize((1, 1)).getcolors()[0][1]
            return [r, g, b]
        RGB_A = None
        if self._base_image is None:
            RGB_A = getRgb(origin)

        RGB_B = getRgb(local)


        # if len(RGB_A) == 3 and len(RGB_B) == 3:
        score = (RGB_A[0] - RGB_B[0]) ** 2 + (RGB_A[1] - RGB_B[1]) ** 2 + (RGB_A[2] - RGB_B[2]) ** 2
        # 需要一个最大数 , 的到百分比
        score = (float(abs(score)) / 195075) * 100

        return score
