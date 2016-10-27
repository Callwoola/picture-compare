# coding:utf-8

from PIL import Image as im
from src.detectors.phash import Phash
from src.detectors.base import Base
from src.detectors.color import Color
from src.detectors.mse import Mse

# 方向 base 的数据其实只需要提取一次啊, 囧~~
class Feature:
    '''
    Compare Image differ I find some useful function
    Maybe Some function would suit for you Project
    '''
    detector = {}

    # 预注册特征
    __default_feature = [
        # 'Phash',
        'Base',
        # 'Color',
        # 'Mse',
    ]

    # 使用比特码对比
    byte_base = None
    byte_storage = None

    # 算法特征
    # 将原对比图片 预先出错 , 避免 重复计算
    base_image_trait_for_image = None
    base_image_trait_for_cv = None

    def __init__(self):
        # 注册所有的特征
        self.__reg(Phash())
        self.__reg(Base())
        self.__reg(Color())
        self.__reg(Mse())

    def __reg(self, instance_name = None):
        self.detector[
            instance_name.get_name()
        ] = instance_name

    def process(self, detector_list = []):
        '''
        : 每个进程都会使用这个 Process,  出现了一些问题??
        '''
        if (detector_list is None) or (not len(detector_list) > 0):
            detector_list = self.__default_feature

        result = {}
        for single_feature in self.detector:
            if single_feature in detector_list:
                result[single_feature] = self.detector[single_feature].calculate(
                    self.byte_base,
                    self.byte_storage
                )
        return result

    def set_byte_base_image(self, byte):
        self.byte_base = byte

    def set_byte_storage_image(self, byte):
        self.byte_storage = byte
