# coding:utf-8
import math
import operator
from PIL import Image as im
from src.detector import Detector

# histogram 算法
class Base(Detector):

    def calculate(self, origin = None, local = None):
        return self._base(origin, local)

    # ----------------------------------------------------------
    # base
    # 算法 -> 直方图比较
    # ----------------------------------------------------------
    def _base(self, origin = None, local = None):
        # origin 需要 静态化
        if self._base_image is None:
            print 'histogram calculate'
            image1 = im.open(origin)
            self._base_image = image1.convert('RGB').histogram()

        # if not image1.size is image2.size:
        #     image2 = image2.resize(image1.size)
        # pass

        image2 = im.open(local)
        h2 = image2.convert('RGB').histogram()

        rms = math.sqrt(
            reduce(
                operator.add,
                list(
                    map(
                        lambda a, b: (a - b) ** 2, self._base_image, h2
                    )
                )
            )
            /
            len(self._base_image)
        )
        print rms
        # 如果这个  histigram 波浪太大就过滤掉
        # wave = reduce(lambda o,n: abs(0-n),image2.convert('RGB').histogram())
        # return wave

        return rms
