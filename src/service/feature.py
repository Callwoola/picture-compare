# coding:utf-8

from PIL import Image as im
from src.detectors.phash import Phash
from src.detectors.base import Base

# 方向 base 的数据其实只需要提取一次啊, 囧~~
class Feature:
    '''
    Compare Image differ I find some useful function
    Maybe Some function would suit for you Project
    '''
    detector = {}

    def __init__(self):
        # 注册所有的特征
        self.__reg(Phash())
        self.__reg(Base())

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
