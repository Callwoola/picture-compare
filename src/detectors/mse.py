# coding:utf-8

from PIL import Image as im
from src.detector import Detector

class Phash(Detector):

    def calculate(self, origin = None, local = None):
        # 注册 执行 perceptual hash
        return self._mse(origin, local)

    # ----------------------------------------------------------
    # mse 均方误差
    # MSE可以评价数据的变化程度，MSE的值越小，说明预测模型描述实验数据具有更好的精确度。与此相对应的，还有均方根误差RMSE、平均绝对百分误差等等。
    # ----------------------------------------------------------
    def _mse(self,  origin = None, local = None):
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
