# coding:utf-8

from PIL import Image as im
from src.detector import Detector

class Phash(Detector):

    def calculate(self, origin = None, local = None):
        # 注册 执行 perceptual hash
        return self._mse(origin, local)

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
