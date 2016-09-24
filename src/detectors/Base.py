# coding:utf-8

from PIL import Image as im
from src.detector import Detector

class Base(Detector):

    def calculate(self, origin = None, local = None):
        # 注册 执行 perceptual hash
        return self._base(origin, local)


    # ----------------------------------------------------------
    # base
    # 算法 -> 直方图比较
    # ----------------------------------------------------------
    def _base(self, origin = None, local = None):
        image1 = im.open(self.byte_base)
        image2 = im.open(self.byte_storage)

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
