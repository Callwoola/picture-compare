# coding:utf-8

import io

# define a base detector Image paser for module
class Detector:
    _weight = 1
    # 储存 原 对比数据, 避免又一次计算
    _base_image = None
    _base_image_for_opencv = None
    # 注册名称
    def get_name(self):
        return self.__class__.__name__

    def __init__(self):
        pass
        
    def match(self, source, target):
        source_path = source.get_path()
        target_path = target.get_path()
        
    def do_screening(self):
        raise Exception('You must rewrite the do screening function!!')
    
    def get_score(self):
        return self.do_screening()

    # def reg(self):
    #     # 注册该方法到 feature
    #     raise Exception('You must rewrite the do screening function!!')

    def calculate(self, origin = None, local = None):
        # 开始计算
        raise Exception('You must rewrite the calculate function!!')

    def is_io(self, io_image = None):
        if io is None:
            raise Exception('io is error')
        if not isinstance(io_image, io.BytesIO):
            return False
        return True
